from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class LeadSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("LeadResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Lead", {
                "id": fields.Integer,
                "name": fields.String,
                "period": fields.Date,
                "description": fields.String,
                "contact_id": fields.Integer,
                "partner_id": fields.Integer,
                "contact": fields.Nested(namespace.model("LeadContact", {
                    "id": fields.Integer,
                    "name": fields.String,
                }), allow_null=True),
                "partner": fields.Nested(namespace.model("LeadPartner", {
                    "id": fields.Integer,
                    "name": fields.String,
                }), allow_null=True),
            }))
        })
    
    @classmethod
    def post_schema(cls, namespace: Model):
        return namespace.model("LeadPostRequest", {
            "name": fields.String(required=True, description="Lead name"),
            "period": fields.Date(required=True, description="Lead period (YYYY-MM-DD)"),
            "description": fields.String(required=True, description="Lead description"),
            "contact_id": fields.Integer(required=False, description="Contact ID"),
            "partner_id": fields.Integer(required=False, description="Partner ID"),
        })