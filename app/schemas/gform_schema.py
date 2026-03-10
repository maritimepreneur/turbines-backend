from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class GformSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("GformResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Gform", {
                "id": fields.Integer,
                "url": fields.String,
                "name": fields.String,
                "batch": fields.Integer,
                "date": fields.String(description="ISO 8601 Date"),
                "type": fields.String(description="GformType Enum"),
                "category": fields.String,
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
        return namespace.model("GformPostRequest", {
            "url": fields.String(required=True, description="Google Form URL"),
            "name": fields.String(required=True, description="Form Name"),
            "batch": fields.Integer(required=True, description="Batch Number"),
            "date": fields.String(required=True, description="Format: YYYY-MM-DD"),
            "type": fields.String(required=True, description="Traning Course Registraion, Training Course Scholarship, Others"),
            "category": fields.String(required=True, description="Category Name"),
        })

    @classmethod
    def filter_schema(cls, namespace: Model):
        """Schema untuk Request Body Search & Filter Gform"""
        return namespace.model("GformFilterRequest", {
            "page_size": fields.Integer(required=True, default=25),
            "page_number": fields.Integer(required=True, default=1),
            "sort_by": fields.String(required=True, default="id"),
            "sort_order": fields.String(required=True, default="DESC"),
            "search": fields.String(description="Search by Name or Category"),
            "type": fields.String(description="Filter by Gform Type Enum"),
            "batch": fields.Integer(description="Filter by Batch Number")
        }, ordered=True)

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema untuk Response List Gform dengan Pagination"""
        gform_item = namespace.model("GformFilterItem", {
            "id": fields.Integer,
            "url": fields.String,
            "name": fields.String,
            "batch": fields.Integer,
            "date": fields.String,
            "type": fields.String,
            "category": fields.String,
            "meta": fields.Nested(namespace.model("Meta", {
                "created_at": fields.String(description="ISO 8601 Date"),
                "updated_at": fields.String(description="ISO 8601 Date"),
                "created_by": fields.Integer,
                "updated_by": fields.Integer,
            })),
        }, ordered=True)

        pagination = namespace.model("GformPaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        }, ordered=True)

        return namespace.model("GformFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(namespace.model("GformFilterData", {
                "list": fields.List(fields.Nested(gform_item)),
                "pagination": fields.Nested(pagination)
            }))
        }, ordered=True)