from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class AgreementSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """Schema for Agreement Details Response"""
        # Buat model internal untuk object 'data'
        agreement_model = namespace.model("Agreement", {
            "id": fields.Integer,
            "name": fields.String,
            "description": fields.String,
            "contact_ids": fields.List(fields.Integer),
            "partner_ids": fields.List(fields.Integer),
            "document": fields.Raw(allow_null=True),
            "meta": fields.Nested(namespace.model("AgreementMeta", {
                "created_at": fields.String,
                "updated_at": fields.String,
                "created_by": fields.Integer,
                "updated_by": fields.Integer,
            })),
        })

        # Bungkus dengan BaseSchema.get_schema
        return namespace.model("AgreementResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(agreement_model)
        })

    @classmethod
    def post_schema(cls, namespace: Model):
        """Schema for Create/Update Agreement Request"""
        return namespace.model("AgreementPostRequest", {
            "name": fields.String,
            "description": fields.String,
            "contact_ids": fields.List(fields.Integer, example=[1, 2]),
            "partner_ids": fields.List(fields.Integer, required=True, example=[1, 3, 5])
        })