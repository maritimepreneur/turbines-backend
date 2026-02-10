from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class QuotationSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("QuotationResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Quotation", {
                "id": fields.Integer,
                "total_amount": fields.String(
                description="Decimal/Numeric amount as string, example 15000.00",
                required=True
                ),
                "document_content": fields.String,
                "summary": fields.String,
                "offering_letter": fields.String,
                "contact": fields.Nested(namespace.model("QuotationContact", {
                    "id": fields.Integer,
                    "name": fields.String,
                    "company": fields.String,
                })),
                "partner": fields.Nested(namespace.model("QuotationPartner", {
                    "id": fields.Integer,
                    "name": fields.String,
                    "service": fields.String,
                    "goods": fields.String,
                })),
                "lead": fields.Nested(namespace.model("QuotationLead", {
                    "id": fields.Integer,
                    "name": fields.String,
                    "period": fields.String,
                    "current_stages": fields.String,
                })),
            }))
        })
    
    @classmethod
    def post_schema(cls, namespace: Model):
        return namespace.model("QuotationPostResponse", {
            "total_amount": fields.String(
                description="Decimal/Numeric amount as string, example 15000.00",
                required=True
            ),
            "document_content": fields.String(required=True),
            "summary": fields.String(required=True),
            "offering_letter": fields.String(required=True),
            "contact_id": fields.Integer(required=False, allow_null=True),
            "partner_id": fields.Integer(required=False, allow_null=True),
            "lead_id": fields.Integer(required=False, allow_null=True),
        })