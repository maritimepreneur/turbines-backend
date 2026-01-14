from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class PartnerSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("PartnerResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Partner", {
                "id": fields.Integer,
                "name": fields.String,
                "initials": fields.String,
                "industrials": fields.String,
                "company_type": fields.String(
                    attribute=lambda x: x.company_type.value if x and x.company_type else None
                ),
                "partner_type": fields.String(
                    attribute=lambda x: x.partner_type.value if x and x.partner_type else None
                ),
                "service": fields.String,
                "goods": fields.String,
            }))
        })
    
    @classmethod
    def post_schema(cls, namespace: Model):
        return namespace.model("PartnerPostResponse", {
            "name": fields.String(required=True),
            "initials": fields.String(required=True),
            "industrials": fields.String(required=True),
            "company_type": fields.String(required=True),
            "partner_type": fields.String(required=True),
            "service": fields.String,
            "goods": fields.String,
        })