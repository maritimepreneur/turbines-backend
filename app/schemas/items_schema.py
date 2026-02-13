from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema


class ItemsSchema(BaseSchema):

    @classmethod
    def create_schema(cls, namespace: Model):
        return namespace.model("ItemsCreate", {
            "name": fields.String(required=True),
            "cost": fields.Float(required=True),
            "amount": fields.Float(required=True),
            "billed_amount": fields.Float(required=True),
            "type": fields.String(required=True),
            "amount_type": fields.String(required=True),
            "attachments": fields.List(fields.Raw, required=False),
            "expense_id": fields.Integer(required=False),
            "quotation_id": fields.Integer(required=False),
        })

    @classmethod
    def response_schema(cls, namespace: Model):
        return namespace.model("ItemsResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Raw
        })
