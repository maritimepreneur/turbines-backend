from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema


class ApprovalSchema(BaseSchema):

    @classmethod
    def get_schema(cls, namespace: Model):
        """Schema untuk Detail Approval (Single Object)"""
        return namespace.model("ApprovalResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Approval", {
                "id": fields.Integer,
                "type": fields.String(
                    description="Approval status: Pending / Approved / Rejected"
                ),
                "code": fields.String(
                    description="Format: QUO-FIN-BD-130226000001"
                ),
                "quotation_id": fields.Integer,
                "po_id": fields.Integer,
                "invoice_id": fields.Integer,
                "expense_id": fields.Integer,
                "lead_id": fields.Integer,
                "meta": fields.Nested(namespace.model("Meta", {
                    "created_at": fields.String(description="ISO 8601 Date"),
                    "updated_at": fields.String(description="ISO 8601 Date"),
                    "created_by": fields.Integer,
                    "updated_by": fields.Integer,
                })),
            }, ordered=True))
        }, ordered=True)

    @classmethod
    def post_schema(cls, namespace: Model):
        """Schema untuk Create Approval"""
        return namespace.model("ApprovalPostRequest", {
            "entity_type": fields.String(
                required=True,
                description="Entity type: Quotation / Purchase Order / Invoice / Expense",
                enum=["Quotation", "Purchase Order", "Invoice", "Expense"]
            ),
            "quotation_id": fields.Integer(required=False, allow_null=True),
            "po_id": fields.Integer(required=False, allow_null=True),
            "invoice_id": fields.Integer(required=False, allow_null=True),
            "expense_id": fields.Integer(required=False, allow_null=True),
        }, ordered=True)

    @classmethod
    def update_schema(cls, namespace: Model):
        """Schema untuk Update Approval Status"""
        return namespace.model("ApprovalUpdateRequest", {
            "type": fields.String(
                required=True,
                enum=["PENDING", "APPROVED", "REJECTED"],
                description="Update approval status"
            )
        }, ordered=True)

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema untuk List Approval dengan Pagination"""

        approval_item_model = namespace.model("ApprovalFilterItem", {
            "id": fields.Integer,
            "type": fields.String,
            "code": fields.String,
            "quotation_id": fields.Integer,
            "po_id": fields.Integer,
            "invoice_id": fields.Integer,
            "expense_id": fields.Integer,
            "lead_id": fields.Integer,
        }, ordered=True)

        return namespace.model("ApprovalFilterResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("ApprovalFilterData", {
                "list": fields.List(fields.Nested(approval_item_model)),
                "pagination": fields.Nested(namespace.model("ApprovalPagination", {
                    "current_page": fields.Integer,
                    "page_size": fields.Integer,
                    "total_pages": fields.Integer,
                    "total_items": fields.Integer
                }))
            }))
        }, ordered=True)