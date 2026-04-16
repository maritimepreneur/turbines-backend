from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_
from flask_jwt_extended import get_jwt_identity
from app.services.base_service import BaseService
from app.models.purchase_orders import Purchase_Order
from app.models.partners import Partner
from app.models.contacts import Contact
from app.models.quotations import Quotation
from app.utils import response
from app.services.approval_service import ApprovalService

class PurchaseOrderService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Purchase_Order)

    def create_purchase(self, data):
        purchase_type = data.pop("type", None) 
        partner_id = data.get("partner_id")

        partner = self.db.query(Partner).get(partner_id)
        if not partner:
            raise ValueError("Partner not found")

        data["number"] = self.generate_purchase_number(partner.initials, purchase_type)

        try:
            new_po = Purchase_Order(**data)
            self.db.add(new_po)
            self.db.flush()
            self.db.refresh(new_po)
            print(f"DEBUG >>> new_po.id={new_po.id}, created_by={new_po.created_by}")

            approval_service = ApprovalService(self.db)
            approval_payload = {
                "entity_type": "Purchase Order",
                "po_id": new_po.id,
                "quotation_id": 0,
                "invoice_id": 0,
                "expense_id": 0,
                "creator_id": new_po.created_by,
                "is_internal": True
            }
           
            approval_result = approval_service.create(approval_payload)

            result_data = new_po.to_dict() 
            
            if approval_result and "data" in approval_result:
                result_data["approval_code"] = approval_result["data"].get("code")

            self.db.commit()
            
            return {"code": 201, "message": "Success", "data": result_data}

        except Exception as e:
            self.db.rollback()
            print(f"ATOMIC TRANSACTION FAILED: {str(e)}")
            raise e 

    def generate_purchase_number(self, initials, purchase_type):
        type_mapping = {
            "service": "SVC",
            "goods": "GDS"
        }

        type_code = type_mapping.get(purchase_type.lower())
        if not type_code:
            raise ValueError("type must be 'service' or 'goods'")

        prefix = f"PO-{initials}-{type_code}-"

        last_purchase = (
            self.db.query(Purchase_Order)
            .filter(Purchase_Order.number.ilike(f"{prefix}%"))
            .order_by(desc(Purchase_Order.number))
            .first()
        )

        if not last_purchase:
            new_increment = 1
        else:
            try:
                last_number = last_purchase.number.split("-")[-1]
                new_increment = int(last_number) + 1
            except (ValueError, IndexError):
                new_increment = 1

        return f"{prefix}{new_increment:06d}"

    def update_purchase(self, id, data):
        data.pop("number", None)
        data.pop("type", None)  
        return self.update(id, data)

    def get_purchase_order_list_filter(self, payload):
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')

            partner_ids = payload.get('partner_ids', [])
            quotation_ids = payload.get('quotation_ids', [])

            query = self.db.query(Purchase_Order)\
                .outerjoin(Partner, Purchase_Order.partner_id == Partner.id)\
                .outerjoin(Quotation, Purchase_Order.quotation_id == Quotation.id)\
                .outerjoin(Contact, Purchase_Order.contact_id == Contact.id)

            if search_query:
                query = query.filter(
                    or_(
                        Purchase_Order.number.ilike(f"%{search_query}%"),
                        Partner.name.ilike(f"%{search_query}%")
                    )
                )

            if partner_ids:
                query = query.filter(Purchase_Order.partner_id.in_(partner_ids))

            if quotation_ids:
                query = query.filter(Purchase_Order.quotation_id.in_(quotation_ids))

            sort_column = getattr(Purchase_Order, sort_by) \
                if hasattr(Purchase_Order, sort_by) else Purchase_Order.id

            query = query.order_by(
                desc(sort_column) if sort_order.upper() == 'DESC'
                else asc(sort_column)
            )

            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size

            raw_data = query.offset(offset).limit(page_size).all()

            data_list = []
            for po in raw_data:
                item = po.to_dict()
                item["partner_name"] = po.partner.name if po.partner else None
                item["contact_name"] = po.contact.name if po.contact else None
                item["quotation_summary"] = po.quotation.summary if po.quotation else None
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
            return response(500, f"Error processing purchase order filter: {str(e)}")