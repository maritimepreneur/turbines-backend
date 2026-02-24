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
                "meta": fields.Nested(namespace.model("Meta", {
                    "created_at": fields.String(description="ISO 8601 Date"),
                    "updated_at": fields.String(description="ISO 8601 Date"),
                    "created_by": fields.Integer,
                    "updated_by": fields.Integer,
                })),
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

    @classmethod
    def filter_schema(cls, namespace: Model):
        """Schema untuk Request Body Search & Filter Expense"""
        return namespace.model("ExpenseFilterRequest", {
            "page_size": fields.Integer(required=True, default=25),
            "page_number": fields.Integer(required=True, default=1),
            "sort_by": fields.String(required=True, default="id"),
            "sort_order": fields.String(required=True, default="DESC"),
            "search": fields.String(description="Search by Expense Code or Notes"),
            "statuses": fields.List(fields.String, description="Filter by multiple statuses (e.g., PENDING, APPROVED)"),
            "period_start": fields.String(description="Start Date (YYYY-MM-DD)"),
            "period_end": fields.String(description="End Date (YYYY-MM-DD)"),
            "min_amount": fields.Float(description="Minimum total amount"),
            "max_amount": fields.Float(description="Maximum total amount")
        }, ordered=True)

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema untuk List Response dengan Pagination"""
        expense_item_model = namespace.model("ExpenseFilterItem", {
            "id": fields.Integer,
            "period_date": fields.String,
            "code": fields.String,
            "status": fields.String,
            "total_amount": fields.String,
            "notes": fields.String,
            "meta": fields.Nested(namespace.model("Meta", {
                    "created_at": fields.String(description="ISO 8601 Date"),
                    "updated_at": fields.String(description="ISO 8601 Date"),
                    "created_by": fields.Integer,
                    "updated_by": fields.Integer,
                })),
        }, ordered=True)

        pagination_model = namespace.model("ExpensePaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        }, ordered=True)

        return namespace.model("ExpenseFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(namespace.model("ExpenseFilterData", {
                "list": fields.List(fields.Nested(expense_item_model)),
                "pagination": fields.Nested(pagination_model)
            }))
        }, ordered=True)