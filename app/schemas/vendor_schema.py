from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class VendorSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("VendorResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.List(
                fields.Nested(
                    namespace.model("Vendor", {
                        "id": fields.Integer,
                        "name": fields.String,
                        "initials": fields.String,
                        "industry": fields.String,
                        "company_type": fields.String,
                        "partner_type": fields.String,
                        "service": fields.List(fields.String),
                        "goods": fields.List(fields.String),
                        "created_at": fields.String
                    })
                )
            )
        })
