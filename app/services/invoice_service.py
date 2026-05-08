from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc, asc, cast, String
from app.models.invoices import Invoice
from app.models.contacts import Contact
from app.models.partners import Partner
from app.models.quotations import Quotation
from app.models.approvals import Approval, ApprovalStatus, ApprovalType
from app.models.purchase_orders import Purchase_Order
from app.services.base_service import BaseService
from app.utils import response
from datetime import datetime, date
from sqlalchemy import desc

def generate_invoice_number(db, items):

    if not items:
        raise ValueError("Items cannot be empty for invoice")

    # ambil semua type
    types = set(
        item.type.value if hasattr(item.type, "value") else item.type
        for item in items
    )

    # VALIDASI: tidak boleh campur
    if len(types) > 1:
        raise ValueError("Invoice cannot contain mixed item types (Service & Goods)")

    item_type = list(types)[0]

    type_map = {
        "Service": "SVC",
        "Goods": "GDS"
    }

    type_code = type_map.get(item_type)

    if not type_code:
        raise ValueError("Invalid item type")

    prefix = f"INV-{type_code}-"

    # cari last number
    last_invoice = (
        db.query(Invoice)
        .filter(Invoice.number.like(f"{prefix}%"))
        .order_by(desc(Invoice.number))
        .first()
    )

    if not last_invoice:
        increment = 1
    else:
        last_number = last_invoice.number.split("-")[-1]
        increment = int(last_number) + 1

    return f"{prefix}{str(increment).zfill(6)}"


class InvoiceService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Invoice)

    def get_all_invoices(self):
        """ Get all Invoices """
        invoices = self.db.query(Invoice).all()
        data = [inv.to_dict() for inv in invoices]
        return response(200, "Success", data)
    
    def calculate_invoice_amount(self, items, data, quotation):
    
        # AMBIL DARI QUOTATION (SOURCE OF TRUTH)
        total_amount = float(quotation.total_amount or 0)

        # billed tetap dari items
        total_billed = sum(float(i.billed_amount or 0) for i in items)

        VAT_PERCENT = 11
        PPH_PERCENT = 2.5

        vat = total_amount * VAT_PERCENT / 100
        pph = total_amount * PPH_PERCENT / 100

        overheads = float(data.get("overheads", 0))
        discount = float(data.get("discount", 0))

        grand_total = total_amount + vat + overheads - discount - pph

        return {
            "total_amount": total_amount,
            "billed_amount": total_billed,
            "vat": vat,
            "pph": pph,
            "grand_total": grand_total
        }

    def create_invoice(self, data):

        error = self.validate_fk(data)
        if error:
            return error

        try:
            user_id = self.get_user_id_login()
            if not user_id:
                return response(401, "Unauthorized")

            # VALIDASI PO
            po_id = data.get("purchase_order_id")
            if not po_id:
                return response(400, "Purchase Order is required")

            po = self.db.get(Purchase_Order, po_id)
            if not po:
                return response(404, "Purchase Order not found")

            if not po.quotation:
                return response(400, "PO has no quotation")

            items = po.quotation.items
            if not items:
                return response(400, "PO has no items")

            # GENERATE NUMBER
            try:
                data["number"] = generate_invoice_number(self.db, items)
            except ValueError as e:
                return response(400, str(e))

            # CALCULATE
            calc = self.calculate_invoice_amount(
                items,
                data,
                po.quotation
            )

            # MERGE DATA
            data.update({
                "contact_id": po.contact_id,
                "partner_id": po.partner_id,
                **calc
            })

            # CREATE INVOICE
            invoice = Invoice(**data)
            invoice.created_by = user_id
            invoice.updated_by = user_id

            self.db.add(invoice)
            self.db.flush()

            # CREATE APPROVAL
            from app.services.approval_service import ApprovalService
            approval_service = ApprovalService(self.db)
            approval_data = {
                "entity_type": "Invoice",
                "invoice_id": invoice.id
            }
            approval_service.create_internal(approval_data, user_id)

            self.db.commit()

            return response(201, "Created", invoice)

        except Exception as e:
            self.db.rollback()
            return response(500, str(e))

    def get_invoice_by_id(self, invoice_id):
        invoice = (
            self.db.query(Invoice)
            .options(
                joinedload(Invoice.purchase_order)
                .joinedload(Purchase_Order.quotation)
                .joinedload(Quotation.items),
                joinedload(Invoice.approval)
            )
            .filter(Invoice.id == invoice_id)
            .first()
        )

        if not invoice:
            return response(404, "Invoice not found")

        data = invoice.to_dict()

        # inject items dari PO
        if invoice.purchase_order and invoice.purchase_order.quotation:
            data["items"] = [
                item.to_dict()
                for item in invoice.purchase_order.quotation.items
            ]
        else:
            data["items"] = []

        return response(200, "Success", data)

    def update_invoice(self, invoice_id, updated_data):
        invoice = self._get_by_id(invoice_id)
        if not invoice:
            return response(404, "Invoice not found")

        validation = self.validate_fk(updated_data)
        if validation:
            return validation

        # BLOCK ITEM EDIT
        if "items" in updated_data:
            return response(400, "Items cannot be modified for invoice")

        user_id = self.get_user_id_login()

        try:
            # UPDATE FIELD BIASA
            for key, value in updated_data.items():
                setattr(invoice, key, value)

            invoice.updated_by = user_id

            # RE-CALCULATE (WAJIB)
            if invoice.purchase_order and invoice.purchase_order.quotation:
                items = invoice.purchase_order.quotation.items

                calc = self.calculate_invoice_amount(
                    items,
                    {
                        "overheads": invoice.overheads,
                        "discount": invoice.discount
                    },
                    invoice.purchase_order.quotation
                )

                invoice.total_amount = calc["total_amount"]
                invoice.billed_amount = calc["billed_amount"]
                invoice.vat = calc["vat"]
                invoice.pph = calc["pph"]
                invoice.grand_total = calc["grand_total"]

            # RESET APPROVAL
            if invoice.approval:
                invoice.approval.status = ApprovalStatus.PENDING
                invoice.approval.updated_by = user_id

            self.db.commit()

            return response(200, "Updated", invoice)

        except Exception as e:
            self.db.rollback()
            return response(500, str(e))

    def delete_invoice(self, invoice_id):
        """ Delete Invoice """
        return super().delete(invoice_id)

    def validate_fk(self, data):
        """ Helper untuk validasi Foreign Keys """
        if data.get("contact_id") and not self.db.query(Contact).get(data["contact_id"]):
            return response(404, "Invalid contact_id")
        
        if data.get("partner_id") and not self.db.query(Partner).get(data["partner_id"]):
            return response(404, "Invalid partner_id")
            
        if data.get("purchase_order_id") and not self.db.query(Purchase_Order).get(data["purchase_order_id"]):
            return response(404, "Invalid purchase_order_id")
        
        return None

    def get_invoice_list_filter(self, payload):
        """NEW: Search, Filter, and Pagination for Invoices"""
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')
            partner_ids = payload.get('partner_ids', [])
            start_date = payload.get('start_date')
            end_date = payload.get('end_date')
            min_amount = payload.get('min_amount')
            max_amount = payload.get('max_amount')

            query = self.db.query(Invoice)\
                .outerjoin(Partner, Invoice.partner_id == Partner.id)\
                .outerjoin(Contact, Invoice.contact_id == Contact.id)\
                .outerjoin(Purchase_Order, Invoice.purchase_order_id == Purchase_Order.id)

            if search_query:
                query = query.filter(
                    or_(
                        cast(Invoice.number, String).ilike(f"%{search_query}%"),
                        Partner.name.ilike(f"%{search_query}%"),
                        Purchase_Order.number.ilike(f"%{search_query}%")
                    )
                )

            if partner_ids:
                query = query.filter(Invoice.partner_id.in_(partner_ids))
            if start_date and end_date:
                query = query.filter(Invoice.period.between(start_date, end_date))
            elif start_date:
                query = query.filter(Invoice.period >= start_date)
            elif end_date:
                query = query.filter(Invoice.period <= end_date)
            if min_amount is not None:
                query = query.filter(Invoice.total_amount >= min_amount)
            if max_amount is not None:
                query = query.filter(Invoice.total_amount <= max_amount)

            sort_column = getattr(Invoice, sort_by) if hasattr(Invoice, sort_by) else Invoice.id
            query = query.order_by(desc(sort_column) if sort_order.upper() == 'DESC' else asc(sort_column))
            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            raw_data = query.offset(offset).limit(page_size).all()
            
            data_list = []
            for inv in raw_data:
                item = inv.to_dict()
                item["partner_name"] = inv.partner.name if inv.partner else None
                item["contact_name"] = inv.contact.name if inv.contact else None
                item["po_number"] = inv.purchase_order.number if inv.purchase_order else None
                data_list.append(item)

            result = {
                "list": data_list,
                "pagination": {
                    "current_page": page_number,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "total_items": total_items
                }
            }
            return response(200, "Success", result)

        except Exception as e:
            return response(500, f"Error processing invoice filter: {str(e)}")