from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc, cast, String
from app.models.invoices import Invoice
from app.models.contacts import Contact
from app.models.partners import Partner
from app.models.purchase_orders import Purchase_Order
from app.services.base_service import BaseService
from app.utils import response

class InvoiceService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Invoice)

    def get_all_invoices(self):
        """ Get all Invoices """
        invoices = self.db.query(Invoice).all()
        data = [inv.to_dict() for inv in invoices]
        return response(200, "Success", data)

    def create_invoice(self, data):
        """ Create a new Invoice """
        validation = self.validate_fk(data)
        if validation:
            return validation
            
        existing = self.db.query(Invoice).filter(Invoice.number == data.get('number')).first()
        if existing:
            return response(400, "Invoice number already exists")

        return super().create(data)

    def get_invoice_by_id(self, invoice_id):
        """ Get Invoice details """
        invoice = self._get_by_id(invoice_id)
        if not invoice:
            return response(404, "Invoice not found", None)
        return response(200, "Success", invoice.to_dict())

    def update_invoice(self, invoice_id, updated_data):
        """ Update Invoice """
        invoice = self._get_by_id(invoice_id)
        if not invoice:
            return response(404, "Invoice not found", None)

        validation = self.validate_fk(updated_data)
        if validation:
            return validation

        if 'number' in updated_data and updated_data['number'] != invoice.number:
                existing = self.db.query(Invoice).filter(Invoice.number == updated_data['number']).first()
        if existing:
                return response(400, "Invoice number already exists")

        return super().update(invoice_id, updated_data)

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