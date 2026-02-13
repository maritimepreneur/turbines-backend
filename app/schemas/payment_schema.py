from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class PaymentSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """Schema untuk Detail Payment (Single Object)"""
        return namespace.model("PaymentResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Payment", {
                "id": fields.Integer,
                "date": fields.String,
                "nominal": fields.Float,
                "notes": fields.String,
                "attachments": fields.String,
                "invoice_id": fields.Integer,
                # Relasi Nested
                "invoice": fields.Nested(namespace.model("PaymentInvoice", {
                    "id": fields.Integer,
                    "number": fields.String,
                }), allow_null=True),
            }, ordered=True))
        }, ordered=True)

    @classmethod
    def post_schema(cls, namespace: Model):
        """Schema untuk Create/Update Payment (Payload Request)"""
        return namespace.model("PaymentPostRequest", {
            "date": fields.Date(required=True, description="Tanggal pembayaran (YYYY-MM-DD)"),
            "nominal": fields.Float(required=True, description="Jumlah nominal"),
            "notes": fields.String(description="Catatan pembayaran"),
            "attachments": fields.String(description="Link URL atau path lampiran file"),
            "invoice_id": fields.Integer(required=False, description="ID dari tabel Invoices"),
        }, ordered=True)

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema untuk List Response dengan Pagination"""
        payment_item_model = namespace.model("PaymentFilterItem", {
            "id": fields.Integer,
            "date": fields.String,
            "nominal": fields.Float,
            "notes": fields.String,
            "invoice_number": fields.String,
        }, ordered=True)

        return namespace.model("PaymentFilterResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("PaymentFilterData", {
                "list": fields.List(fields.Nested(payment_item_model)),
                "pagination": fields.Nested(namespace.model("PaymentPagination", {
                    "current_page": fields.Integer,
                    "page_size": fields.Integer,
                    "total_pages": fields.Integer,
                    "total_items": fields.Integer
                }))
            }))
        }, ordered=True)
    
    
