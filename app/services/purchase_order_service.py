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
        purchase_type = data.pop("type", None) 
        partner_id = data.get("partner_id")

        if not purchase_type:
            raise ValueError("type is required")

        if not partner_id:
            raise ValueError("partner_id is required")

        partner = self.db.query(Partner).get(partner_id)
        if not partner:
            raise ValueError("Partner not found")

        initials = partner.initials
        if not initials:
            raise ValueError("Partner does not have initials")

        data["number"] = self.generate_purchase_number(initials, purchase_type)

        return self.create(data)

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