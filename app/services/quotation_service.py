from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc, asc
from app.models.quotations import Quotation
from app.models.contacts import Contact
from app.models.partners import Partner
from app.models.approvals import Approval, ApprovalStatus, ApprovalType
from app.models.leads import Lead
from app.models.items import Item
from app.services.base_service import BaseService
from app.utils import response
from datetime import datetime, date

def generate_date_prefix():
    return datetime.now().strftime("%d%m%y")

def generate_running_number(db, model, prefix_field="code", date_prefix=None):
    last = (
        db.query(model)
        .filter(model.code.like(f"%{date_prefix}%"))
        .order_by(model.id.desc())
        .first()
    )

    if not last:
        return "000001"

    last_code = last.code
    last_number = int(last_code[-6:])
    return str(last_number + 1).zfill(6)

def generate_approval_code(db, jenis="QUO", dari="FIN", ke="BD"):
    date_prefix = generate_date_prefix()
    running = generate_running_number(db, Approval, date_prefix=date_prefix)

    return f"{jenis}-{dari}-{ke}-{date_prefix}{running}"

def generate_item_code(name: str, item_type: str, quotation_id: int, index: int):
    prefix = (name[:3].upper() if name else "XXX").ljust(3, "X")

    type_map = {
        "Service": "SVC",
        "Goods": "GDS"
    }

    type_code = type_map.get(item_type, "UNK")

    return f"{prefix}-{type_code}-{quotation_id}-{str(index).zfill(3)}"

class QuotationService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Quotation)

    def inject_meta(self, obj):
        user_id = self.get_user_id_login()

        obj.created_by = user_id
        obj.updated_by = user_id

        return obj

    def get_all_quotations(self):
        """ Get all Quotation """
        quotations = self.db.query(Quotation).all()
        return response(200, "Success", quotations or [])
    
    def create_quotation(self, quotation_data):
        items_data = quotation_data.pop("items", [])

        try:
            with self.db.begin():

                # VALIDASI FK
                error = self.validate_fk(quotation_data)
                if error:
                    return error

                user_id = self.get_user_id_login()
                if not user_id:
                    return response(401, "Unauthorized")

                # CREATE QUOTATION
                quotation = Quotation(**quotation_data)
                quotation.created_by = user_id
                quotation.updated_by = user_id

                self.db.add(quotation)
                self.db.flush()

                # CREATE ITEMS
                for i, item_data in enumerate(items_data, start=1):
                    item = Item(**item_data)

                    item.created_by = user_id
                    item.updated_by = user_id

                    item.code = generate_item_code(
                        item.name,
                        item.type.value if hasattr(item.type, "value") else item.type,
                        quotation.id,
                        i
                    )

                    quotation.items.append(item)

                # CREATE APPROVAL (1:1 ke quotation)
                approval = Approval(
                    status=ApprovalStatus.PENDING,
                    type=ApprovalType.QUOTATION,
                    code=generate_approval_code(self.db),
                    quotation_id=quotation.id
                )

                approval.created_by = user_id
                approval.updated_by = user_id

                self.db.add(approval)

            return response(201, "Created", quotation)

        except Exception as e:
            return response(500, str(e))
    
    def get_quotation_by_id(self, quotation_id):
        quotation = (
            self.db.query(Quotation)
            .options(
                joinedload(Quotation.items),
                joinedload(Quotation.approval)
            )
            .filter(Quotation.id == quotation_id)
            .first()
        )

        if not quotation:
            return response(404, "Quotation not found")

        return response(200, "Success", quotation)
    
    def update_quotation_by_id(self, quotation_id, updated_data):
        try:
            with self.db.begin():

                # GET DATA + LOCK
                quotation = (
                    self.db.query(Quotation)
                    .options(
                        joinedload(Quotation.items),
                        joinedload(Quotation.approval)
                    )
                    .filter(Quotation.id == quotation_id)
                    .first()
                )

                if not quotation:
                    return response(404, "Quotation not found")

                # VALIDASI FK
                error = self.validate_fk(updated_data)
                if error:
                    return error

                user_id = self.get_user_id_login()
                if not user_id:
                    return response(401, "Unauthorized")

                items_data = updated_data.pop("items", [])

                # UPDATE QUOTATION FIELD
                for key, value in updated_data.items():
                    setattr(quotation, key, value)

                quotation.updated_by = user_id

                # MAP EXISTING ITEMS
                existing_items = {item.id: item for item in quotation.items}
                incoming_ids = []
                existing_code_indices = []

                for existing_item in quotation.items:
                    if not existing_item.code:
                        continue
                    try:
                        existing_code_indices.append(
                            int(str(existing_item.code).rsplit("-", 1)[-1])
                        )
                    except (TypeError, ValueError):
                        continue

                next_item_index = (max(existing_code_indices) + 1) if existing_code_indices else 1

                items_changed = False

                for item_data in items_data:

                    # UPDATE EXISTING
                    if item_data.get("id"):
                        item = existing_items.get(item_data["id"])

                        if not item:
                            return response(404, f"Item {item_data['id']} not found")

                        # detect perubahan
                        if (
                            item.name != item_data["name"] or
                            item.cost != item_data["cost"] or
                            item.amount != item_data["amount"] or
                            item.billed_amount != item_data["billed_amount"] or
                            item.type != item_data["type"] or
                            item.amount_type != item_data["amount_type"]
                        ):
                            items_changed = True

                        item.name = item_data["name"]
                        item.cost = item_data["cost"]
                        item.amount = item_data["amount"]
                        item.billed_amount = item_data["billed_amount"]
                        item.type = item_data["type"]
                        item.amount_type = item_data["amount_type"]

                        item.updated_by = user_id

                        incoming_ids.append(item.id)

                    # CREATE NEW ITEM
                    else:
                        items_changed = True

                        item = Item(**item_data)
                        item.created_by = user_id
                        item.updated_by = user_id

                        item.code = generate_item_code(
                            item.name,
                            item.type.value if hasattr(item.type, "value") else item.type,
                            quotation.id,
                            next_item_index
                        )
                        next_item_index += 1

                        quotation.items.append(item)

                # DELETE ORPHAN
                for item_id, item in existing_items.items():
                    if item_id not in incoming_ids:
                        items_changed = True
                        self.db.delete(item)

                # APPROVAL RESET
                if quotation.approval and items_changed:
                    quotation.approval.status = ApprovalStatus.PENDING
                    quotation.approval.updated_by = user_id

            return response(200, "Updated", quotation)

        except Exception as e:
            return response(500, str(e))
    
    def validate_fk(self, quotation_data):
        """ Existing validation logic """
        if quotation_data.get("contact_id") and not self.db.get(Contact, quotation_data["contact_id"]):
            return response(404, "Invalid contact_id")
        
        if quotation_data.get("partner_id") and not self.db.get(Partner, quotation_data["partner_id"]):
            return response(404, "Invalid partner_id")
        
        if quotation_data.get("lead_id") and not self.db.get(Lead, quotation_data["lead_id"]):
            return response(404, "Invalid lead_id")

    def get_quotation_list_filter(self, payload):
        """ New feature: Search, Filter, and Pagination for Quotations """
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')
            min_amount = payload.get('min_amount')
            max_amount = payload.get('max_amount')
            partner_ids = payload.get('partner_ids', [])

            query = self.db.query(Quotation)\
                .outerjoin(Partner, Quotation.partner_id == Partner.id)\
                .outerjoin(Lead, Quotation.lead_id == Lead.id)\
                .outerjoin(Contact, Quotation.contact_id == Contact.id)

            if search_query:
                query = query.filter(
                    or_(
                        Quotation.summary.ilike(f"%{search_query}%"),
                        Partner.name.ilike(f"%{search_query}%"),
                        Lead.name.ilike(f"%{search_query}%")
                    )
                )

            if min_amount is not None:
                query = query.filter(Quotation.total_amount >= min_amount)
            if max_amount is not None:
                query = query.filter(Quotation.total_amount <= max_amount)

            if partner_ids:
                query = query.filter(Quotation.partner_id.in_(partner_ids))

            sort_column = getattr(Quotation, sort_by) if hasattr(Quotation, sort_by) else Quotation.id
            query = query.order_by(desc(sort_column) if sort_order.upper() == 'DESC' else asc(sort_column))
            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            raw_data = query.offset(offset).limit(page_size).all()
            
            data_list = []
            for q in raw_data:
                item = q.to_dict()
                item["contact_name"] = q.contact.name if q.contact else None
                item["partner_name"] = q.partner.name if q.partner else None
                item["lead_name"] = q.lead.name if q.lead else None
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
            return response(500, f"Error processing quotation filter: {str(e)}")
