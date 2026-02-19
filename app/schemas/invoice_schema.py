from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class InvoiceSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("InvoiceResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Invoice", {
                "id": fields.Integer,
                "number": fields.Integer,
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
                    "po_number": fields.String(attribute="number"), # Asumsi di PO ada field number
                }), allow_null=True),
            }))
        })

    @classmethod
    def post_schema(cls, namespace: Model):
        return namespace.model("InvoicePostRequest", {
            "number": fields.Integer(required=True, description="Unique Invoice Number"),
            "period": fields.String(required=True, description="Format: YYYY-MM-DD"),
            "due_date": fields.String(required=True, description="Format: YYYY-MM-DD"),
            "billed_amount": fields.String(required=True, description="Numeric string, ex: 10000.00"),
            "total_amount": fields.String(required=True, description="Numeric string"),
            "notes": fields.String(required=False),
            "vat": fields.String(required=True, default="0.00"),
            "pph": fields.String(required=True, default="0.00"),
            "overheads": fields.String(required=True, default="0.00"),
            "discount": fields.String(required=True, default="0.00"),
            "grand_total": fields.String(required=True, description="Final calculation"),
            "payment_details": fields.String(required=True, description="Bank account details etc."),
            "agreement_letter": fields.String(required=True, description="URL or Reference to agreement letter"),
            
            "contact_id": fields.Integer(required=False, allow_null=True),
            "partner_id": fields.Integer(required=False, allow_null=True),
            "purchase_order_id": fields.Integer(required=False, allow_null=True),
        })