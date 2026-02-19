from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class PurchaseOrderSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """Schema untuk Detail Purchase Order (Single Object)"""
        return namespace.model("PurchaseOrderResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("PurchaseOrder", {
                "id": fields.Integer,
                "number": fields.String,
                "attachments": fields.String,
                "partner_id": fields.Integer,
                "contact_id": fields.Integer,
                "quotation_id": fields.Integer,
                "partner": fields.Nested(namespace.model("POPartner", {
                    "id": fields.Integer,
                    "name": fields.String,
                }), allow_null=True),
                "contact": fields.Nested(namespace.model("POContact", {
                    "id": fields.Integer,
                    "name": fields.String,
                }), allow_null=True),
                "quotation": fields.Nested(namespace.model("POQuotation", {
                    "id": fields.Integer,
                    "number": fields.String,
                }), allow_null=True),
            }, ordered=True))
        }, ordered=True)

    @classmethod
    def post_schema(cls, namespace: Model):
        """Schema untuk Create/Update Purchase Order (Payload Request)"""
        return namespace.model("PurchaseOrderPostRequest", {
            "attachments": fields.String(required=True, description="Link URL atau path lampiran file"),
            "partner_id": fields.Integer(required=True, description="ID dari tabel Partners"),
            "contact_id": fields.Integer(required=True, description="ID dari tabel Contacts"),
            "quotation_id": fields.Integer(required=True, description="ID dari tabel Quotations"),
            "number": fields.String(readonly=True, description="Auto-generated (Tidak perlu diisi saat Create)")
        }, ordered=True)

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema untuk List Response (Jika kamu butuh fitur GET ALL dengan pagination)"""
        po_item_model = namespace.model("PurchaseOrderFilterItem", {
            "id": fields.Integer,
            "number": fields.String,
            "attachments": fields.String,
            "partner_name": fields.String,
            "contact_name": fields.String,
            "quotation_number": fields.String
        }, ordered=True)

        pagination_model = namespace.model("POPaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        }, ordered=True)

        return namespace.model("PurchaseOrderFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(namespace.model("POFilterData", {
                "list": fields.List(fields.Nested(po_item_model)),
                "pagination": fields.Nested(pagination_model)
            }))
        }, ordered=True)