from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class ExpenseSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("ExpenseResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Expense", {
                "id": fields.Integer,
                "period_date": fields.Date,
                "code": fields.String,
                "status": fields.String(
                    attribute=lambda x: x.status.value if x and x.status else None
                ),
                "total_amount": fields.String(
                description="Decimal/Numeric amount as string, example 15000.00",
                required=True
                ),
                "notes": fields.String,
            }))
        })
    
    @classmethod
    def post_schema(cls, namespace: Model):
        return namespace.model("ExpensePostResponse", {
            "period_date": fields.String(
                required=True,
                example="2026-02-10",
                description="ISO date YYYY-MM-DD"
            ),
            "status": fields.String(required=True),
            "total_amount":  fields.String(required=True),
            "notes": fields.String(required=True),
        })