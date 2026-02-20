from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_
from app.services.base_service import BaseService
from app.models.purchase_orders import Purchase_Order
from app.models.partners import Partner
from app.models.contacts import Contact
from app.models.quotations import Quotation
from app.utils import response

class PurchaseOrderService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Purchase_Order)

    def create_purchase(self, data):
        data['number'] = self.generate_purchase_number()
        return self.create(data)

    def generate_purchase_number(self):
        last_purchase = self.db.query(Purchase_Order).order_by(desc(Purchase_Order.id)).first()
        if not last_purchase:
            new_number = 1
        else:
            new_number = last_purchase.id + 1
        return f"PO-{new_number:04d}"

    def update_purchase(self, id, data):
        data.pop('number', None)
        return self.update(id, data)

    def get_purchase_order_list_filter(self, payload):
        """Search, Filter, and Pagination for Purchase Orders"""
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

            sort_column = getattr(Purchase_Order, sort_by) if hasattr(Purchase_Order, sort_by) else Purchase_Order.id
            query = query.order_by(desc(sort_column) if sort_order.upper() == 'DESC' else asc(sort_column))

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