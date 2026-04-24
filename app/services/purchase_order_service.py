from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, asc, or_
from flask_jwt_extended import get_jwt_identity
from app.services.base_service import BaseService
from app.models.purchase_orders import Purchase_Order
from app.models.partners import Partner
from app.models.contacts import Contact
from app.models.quotations import Quotation
from app.models.approvals import Approval, ApprovalStatus, ApprovalType
from app.utils import response
from app.services.approval_service import ApprovalService

class PurchaseOrderService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Purchase_Order)

    def create_purchase(self, data):
        try:
            payload = dict(data)
            purchase_type = payload.pop("type", None)
            quotation_id = payload.get("quotation_id")

            if not quotation_id:
                raise ValueError("quotation_id is required")

            quotation = (
                self.db.query(Quotation)
                .options(joinedload(Quotation.items))
                .get(quotation_id)
            )
            if not quotation:
                raise ValueError("Quotation not found")

            existing_po = (
                self.db.query(Purchase_Order)
                .filter(Purchase_Order.quotation_id == quotation_id)
                .first()
            )
            if existing_po:
                raise ValueError("Purchase order for this quotation already exists")

            partner = self.db.query(Partner).get(quotation.partner_id)
            if not partner:
                raise ValueError("Partner on quotation not found")
            if not partner.initials:
                raise ValueError("Partner does not have initials")

            if not payload.get("attachments"):
                raise ValueError("attachments is required")

            if not purchase_type:
                purchase_type = self.infer_purchase_type(quotation)

            user_id = self.get_user_id_login()
            number = self.generate_purchase_number(partner.initials, purchase_type)

            purchase_order = Purchase_Order(
                number=number,
                attachments=payload.get("attachments"),
                partner_id=quotation.partner_id,
                contact_id=quotation.contact_id,
                quotation_id=quotation.id,
            )
            purchase_order.created_by = user_id
            purchase_order.updated_by = user_id

            self.db.add(purchase_order)
            self.db.flush()

            approval = Approval(
                status=ApprovalStatus.PENDING,
                type=ApprovalType.PO,
                code=self.generate_po_approval_code(),
                po_id=purchase_order.id,
            )
            approval.created_by = user_id
            approval.updated_by = user_id

            self.db.add(approval)
            self.db.commit()
            self.db.refresh(purchase_order)

            return response(201, "Created", purchase_order)
        except ValueError as e:
            self.db.rollback()
            return response(400, str(e))
        except Exception as e:
            self.db.rollback()
            return response(500, str(e))

    def infer_purchase_type(self, quotation: Quotation):
        type_names = {
            (item.type.name if hasattr(item.type, "name") else str(item.type).upper())
            for item in quotation.items
            if item.type is not None
        }

        if len(type_names) == 1:
            only_type = next(iter(type_names))
            if only_type == "GOODS":
                return "goods"
            if only_type == "SERVICE":
                return "service"

        # Default fallback to goods when item composition is mixed/unknown.
        return "goods"

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

    def generate_po_approval_code(self):
        date_prefix = datetime.now().strftime("%d%m%y")
        last = (
            self.db.query(Approval)
            .filter(Approval.code.like(f"%{date_prefix}%"))
            .order_by(desc(Approval.id))
            .first()
        )

        running_number = 1
        if last and last.code:
            try:
                running_number = int(last.code[-6:]) + 1
            except ValueError:
                running_number = 1

        return f"PO-FIN-BD-{date_prefix}{running_number:06d}"

    def update_purchase(self, id, data):
        data.pop("number", None)
        data.pop("type", None)
        data.pop("partner_id", None)
        data.pop("contact_id", None)
        data.pop("quotation_id", None)
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
