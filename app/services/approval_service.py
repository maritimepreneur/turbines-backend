from sqlalchemy import desc
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from flask import abort

from app.models.approvals import Approval, ApprovalType
from app.models.users import User
from app.models.quotations import Quotation
from app.models.purchase_orders import Purchase_Order
from app.models.invoices import Invoice
from app.models.expenses import Expense


class ApprovalService:

    ENTITY_MAPPING = {
        "Quotation": "QUO",
        "Purchase Order": "PO",
        "Invoice": "INV",
        "Expense": "EXP"
    }

    ROLE_MAPPING = {
        "FINANCE": "FIN",
        "ADMIN": "ADM",
        "BIZDEV": "BD"
    }

    def __init__(self, db_session):
        self.db = db_session

    def create(self, data):

        entity_type = data.get("entity_type")
        if not entity_type:
            raise ValueError("entity_type is required")

        entity_type = entity_type.title().strip()

        if entity_type not in self.ENTITY_MAPPING:
            raise ValueError("Invalid entity_type")

        current_user_id = get_jwt_identity()
        current_user = self.db.query(User).get(current_user_id)

        if not current_user:
            raise ValueError("User not found")

        raw_from_role = current_user.role.name.upper()

        if raw_from_role not in self.ROLE_MAPPING:
            raise ValueError("User role not allowed")

        from_dept = self.ROLE_MAPPING[raw_from_role]

        entity_keys = ["quotation_id", "po_id", "invoice_id", "expense_id"]

        filled = [
            key for key in entity_keys
            if data.get(key) and int(data.get(key)) != 0
        ]

        if len(filled) != 1:
            raise ValueError("Exactly one entity ID must be provided")

        for key in entity_keys:
            if not data.get(key) or int(data.get(key)) == 0:
                data[key] = None

        entity = None

        if data.get("quotation_id"):
            entity = self.db.query(Quotation).get(data["quotation_id"])
        elif data.get("po_id"):
            entity = self.db.query(Purchase_Order).get(data["po_id"])
        elif data.get("invoice_id"):
            entity = self.db.query(Invoice).get(data["invoice_id"])
        elif data.get("expense_id"):
            entity = self.db.query(Expense).get(data["expense_id"])

        if not entity:
            raise ValueError("Referenced entity not found")

        creator_user = self.db.query(User).get(entity.created_by)

        if not creator_user:
            raise ValueError("Creator user not found")

        raw_to_role = creator_user.role.name.upper()

        if raw_to_role not in self.ROLE_MAPPING:
            raise ValueError("Creator role not allowed")

        to_dept = self.ROLE_MAPPING[raw_to_role]

        if from_dept == to_dept:
            raise ValueError("Cannot approve within same department")

        new_code = self.generate_code(entity_type, from_dept, to_dept)

        new_approval = Approval(
            type=ApprovalType.PENDING,
            code=new_code,
            quotation_id=data.get("quotation_id"),
            po_id=data.get("po_id"),
            invoice_id=data.get("invoice_id"),
            expense_id=data.get("expense_id"),
        )

        self.db.add(new_approval)
        self.db.commit()

        return {
            "message": "Approval created successfully",
            "code": 201,
            "status": "success",
            "data": {
                **new_approval.to_dict(),
                "lead_id": self.extract_lead_id(new_approval)
            }
        }

    def generate_code(self, entity_type, from_dept, to_dept):

        entity_prefix = self.ENTITY_MAPPING[entity_type]
        today_str = datetime.now().strftime("%d%m%y")

        prefix = f"{entity_prefix}-{from_dept}-{to_dept}-{today_str}"

        last_approval = (
            self.db.query(Approval)
            .filter(Approval.code.ilike(f"{prefix}%"))
            .order_by(desc(Approval.code))
            .first()
        )

        if not last_approval:
            increment = 1
        else:
            last_number = last_approval.code[-6:]
            increment = int(last_number) + 1

        return f"{prefix}{increment:06d}"

    def get_all(self, page=1, per_page=10):

        pagination = (
            self.db.query(Approval)
            .order_by(desc(Approval.id))
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        data_list = []

        for approval in pagination.items:
            data_list.append({
                **approval.to_dict(),
                "lead_id": self.extract_lead_id(approval)
            })

        return {
            "message": "Success",
            "code": 200,
            "status": "success",
            "data": {
                "list": data_list,
                "pagination": {
                    "current_page": pagination.page,
                    "page_size": pagination.per_page,
                    "total_pages": pagination.pages,
                    "total_items": pagination.total
                }
            }
        }

    def get_by_id(self, approval_id):

        approval = self.db.query(Approval).get(approval_id)

        if not approval:
            abort(404, f"Approval ID {approval_id} not found")

        return {
            "message": "Success",
            "code": 200,
            "status": "success",
            "data": {
                **approval.to_dict(),
                "lead_id": self.extract_lead_id(approval)
            }
        }

    def update(self, approval_id, data):

        approval = self.db.query(Approval).get(approval_id)

        if not approval:
            abort(404, f"Approval ID {approval_id} not found")

        if "type" not in data:
            raise ValueError("type is required")

        try:
            approval.type = ApprovalType(data["type"])
        except ValueError:
            raise ValueError("Invalid approval status")

        self.db.commit()

        return {
            "message": "Approval updated successfully",
            "code": 200,
            "status": "success",
            "data": {
                **approval.to_dict(),
                "lead_id": self.extract_lead_id(approval)
            }
        }

    def delete(self, approval_id):

        approval = self.db.query(Approval).get(approval_id)

        if not approval:
            abort(404, f"Approval ID {approval_id} not found")

        self.db.delete(approval)
        self.db.commit()

        return {
            "message": "Approval deleted successfully",
            "code": 200,
            "status": "success"
        }

    def extract_lead_id(self, approval):

        if approval.quotations:
            return approval.quotations.lead_id

        if approval.purchase_orders and approval.purchase_orders.quotation:
            return approval.purchase_orders.quotation.lead_id

        if (
            approval.invoices
            and approval.invoices.purchase_order
            and approval.invoices.purchase_order.quotation
        ):
            return approval.invoices.purchase_order.quotation.lead_id

        if (
            approval.expense
            and approval.expense.invoice
            and approval.expense.invoice.purchase_order
            and approval.expense.invoice.purchase_order.quotation
        ):
            return approval.expense.invoice.purchase_order.quotation.lead_id

        return None