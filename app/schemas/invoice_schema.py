from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class InvoiceSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("InvoiceResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Invoice", {
                "id": fields.Integer,
                "number": fields.String, # Diperbaiki menjadi String
                "created": fields.String(description="ISO 8601 Datetime"),
                "period": fields.String(description="ISO 8601 Date"),
                "due_date": fields.String(description="ISO 8601 Date"),
                "billed_amount": fields.String(description="Numeric string"),
                "total_amount": fields.String(description="Numeric string"),
                "notes": fields.String,
                "vat": fields.String(description="Numeric string"),
                "pph": fields.String(description="Numeric string"),
                "overheads": fields.String(description="Numeric string"),
                "discount": fields.String(description="Numeric string"),
                "grand_total": fields.String(description="Numeric string"),
                "payment_details": fields.String,
                "agreement_letter": fields.String,
                "contact": fields.Nested(namespace.model("InvoiceContact", {
                    "id": fields.Integer,
                    "name": fields.String,
                    "company": fields.String,
                }), allow_null=True),
                "partner": fields.Nested(namespace.model("InvoicePartner", {
                    "id": fields.Integer,
                    "name": fields.String,
                }), allow_null=True),
                "purchase_order": fields.Nested(namespace.model("InvoicePO", {
                    "id": fields.Integer,
                    "po_number": fields.String(attribute="number"),
                }), allow_null=True),
                "approval": fields.Nested(namespace.model("InvoiceApproval", {
                    "id": fields.Integer,
                    "code": fields.String,
                    "status": fields.String(attribute=lambda x: x.status.value if x and x.status else None),
                    "type": fields.String(attribute=lambda x: x.type.value if x and x.type else None),
                }), allow_null=True),
                "meta": fields.Nested(namespace.model("Meta", {
                    "created_at": fields.String(description="ISO 8601 Date"),
                    "updated_at": fields.String(description="ISO 8601 Date"),
                    "created_by": fields.Integer,
                    "updated_by": fields.Integer,
                })),
            }))
        })

    @classmethod
    def post_schema(cls, namespace: Model):
        return namespace.model("InvoicePostRequest", {
            "period": fields.String(required=True, description="Format: YYYY-MM-DD"),
            "due_date": fields.String(required=True, description="Format: YYYY-MM-DD"),
            "notes": fields.String(required=False),
            "overheads": fields.String(required=True, default="0.00"),
            "discount": fields.String(required=True, default="0.00"),
            "payment_details": fields.String(required=True, description="Bank account details etc."),
            "agreement_letter": fields.String(required=True, description="URL or Reference to agreement letter"),
            "purchase_order_id": fields.Integer(required=False, allow_null=True),
        })

    @classmethod
    def filter_schema(cls, namespace: Model):
        """Schema untuk Request Body Search & Filter Invoice"""
        return namespace.model("InvoiceFilterRequest", {
            "page_size": fields.Integer(required=True, default=25),
            "page_number": fields.Integer(required=True, default=1),
            "sort_by": fields.String(required=True, default="id"),
            "sort_order": fields.String(required=True, default="DESC"),
            "search": fields.String(description="Search by Invoice Number, PO Number, or Partner Name"),
            "partner_ids": fields.List(fields.Integer, description="Filter by multiple Partner IDs"),
            "start_date": fields.String(description="Start Date (YYYY-MM-DD) for Period"),
            "end_date": fields.String(description="End Date (YYYY-MM-DD) for Period"),
            "min_amount": fields.Float(description="Minimum total amount"),
            "max_amount": fields.Float(description="Maximum total amount")
        }, ordered=True)

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema untuk List Response dengan Pagination"""
        invoice_item_model = namespace.model("InvoiceFilterItem", {
            "id": fields.Integer,
            "number": fields.String, # Diperbaiki menjadi String
            "period": fields.String,
            "due_date": fields.String,
            "total_amount": fields.String,
            "grand_total": fields.String,
            "partner_name": fields.String,
            "contact_name": fields.String,
            "po_number": fields.String,
            "meta": fields.Nested(namespace.model("Meta", {
                    "created_at": fields.String(description="ISO 8601 Date"),
                    "updated_at": fields.String(description="ISO 8601 Date"),
                    "created_by": fields.Integer,
                    "updated_by": fields.Integer,
                })),
        }, ordered=True)

        pagination_model = namespace.model("InvoicePaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        }, ordered=True)

        return namespace.model("InvoiceFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(namespace.model("InvoiceFilterData", {
                "list": fields.List(fields.Nested(invoice_item_model)),
                "pagination": fields.Nested(pagination_model)
            }))
        }, ordered=True)