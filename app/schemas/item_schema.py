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

    @classmethod
    def filter_schema(cls, namespace: Model):
        """NEW: Schema untuk Request Body Search & Filter Items"""
        return namespace.model("ItemsFilterRequest", {
            "page_size": fields.Integer(required=True, default=25),
            "page_number": fields.Integer(required=True, default=1),
            "sort_by": fields.String(required=True, default="id"),
            "sort_order": fields.String(required=True, default="DESC"),
            "search": fields.String(description="Search by Item Name or Type"),
            "expense_ids": fields.List(fields.Integer, description="Filter by Expense IDs"),
            "quotation_ids": fields.List(fields.Integer, description="Filter by Quotation IDs")
        }, ordered=True)

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """NEW: Schema untuk Response List dengan Pagination"""
        item_filter_model = namespace.model("ItemsFilterItem", {
            "id": fields.Integer,
            "name": fields.String,
            "cost": fields.Float,
            "amount": fields.Float,
            "billed_amount": fields.Float,
            "type": fields.String,
            "amount_type": fields.String,
            "expense_id": fields.Integer,
            "quotation_id": fields.Integer
        }, ordered=True)

        pagination_model = namespace.model("ItemsPaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        }, ordered=True)

        return namespace.model("ItemsFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(namespace.model("ItemsFilterData", {
                "list": fields.List(fields.Nested(item_filter_model)),
                "pagination": fields.Nested(pagination_model)
            }))
        }, ordered=True)