from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class ContactSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("ContactResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Contact", {
                "id": fields.Integer,
                "name": fields.String,
                "email": fields.String,
                "phone_number": fields.String,
                "company": fields.String,
            }))
        })
    
    @classmethod
    def post_schema(cls, namespace: Model):
        return namespace.model("ContactPostResponse", {
            "name": fields.String(required=True),
            "email": fields.String(required=True),
            "phone_number": fields.String(required=True),
            "company": fields.String,
        })