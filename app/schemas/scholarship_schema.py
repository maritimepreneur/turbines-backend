from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class ScholarshipSchema(BaseSchema):

    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("ScholarshipResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Scholarship", {
                "id": fields.Integer,
                "name": fields.String,
                "status": fields.String,
                "date": fields.String,
                "type": fields.String,
                "category": fields.String,
                "original_price": fields.Float,
                "discount": fields.Integer,
                "price": fields.Float,
                "code": fields.String,
                "meta": fields.Nested(namespace.model("Meta", {
                    "created_at": fields.String(description="ISO 8601 Date"),
                    "updated_at": fields.String(description="ISO 8601 Date"),
                    "created_by": fields.Integer,
                    "updated_by": fields.Integer,
                }))
            }, ordered=True))
        }, ordered=True)

    @classmethod
    def item_schema(cls, namespace: Model):
        return namespace.model("ScholarshipItem", {
            "id": fields.Integer,
            "name": fields.String,
            "status": fields.String(attribute=lambda x: x.status.value if x and x.status else None),
            "date": fields.String,
            "type": fields.String,
            "category": fields.String,
            "original_price": fields.Float,
            "discount": fields.Integer,
            "price": fields.Float,
            "code": fields.String,
            "meta": fields.Nested(namespace.model("MetaItem", {
                "created_at": fields.String(description="ISO 8601 Date"),
                "updated_at": fields.String(description="ISO 8601 Date"),
                "created_by": fields.Integer,
                "updated_by": fields.Integer,
            }))
        }, ordered=True)

    @classmethod
    def post_schema(cls, namespace: Model):
        return namespace.model("ScholarshipPostRequest", {
            "name": fields.String(required=True),
            "date": fields.Date(required=True),
            "type": fields.String(required=True),
            "category": fields.String(required=True),
            "original_price": fields.Float(required=True),
            "discount": fields.Integer(required=True)
        }, ordered=True)
    
    @classmethod
    def update_schema(cls, namespace: Model):
        return namespace.model("ScholarshipUpdateRequest", {
            "name": fields.String(),
            "date": fields.Date(),
            "status": fields.String(description="ACTIVE or DEACTIVE"),
            "type": fields.String(),
            "category": fields.String(),
            "original_price": fields.Float(),
            "discount": fields.Integer()
        }, ordered=True)
    
    @classmethod
    def filter_schema(cls, namespace: Model):
        return namespace.model("ScholarshipFilterRequest", {
            "page_size": fields.Integer(default=25),
            "page_number": fields.Integer(default=1),
            "search": fields.String(description="Search by Name, Code, Type, or Category"),
            "status": fields.String(description="ACTIVE or DEACTIVE"),
            "category": fields.String(description="Filter by Category"),
            "type": fields.String(description="Filter by Type"),
            "min_price": fields.Float(description="Minimum Price"),
            "max_price": fields.Float(description="Maximum Price"),
            "sort_by": fields.String(default="id"),
            "sort_order": fields.String(default="DESC")
        }, ordered=True)
    
    @classmethod
    def filter_response_schema(cls, namespace: Model):

        scholarship_item = namespace.model("ScholarshipFilterItem", {
            "id": fields.Integer,
            "name": fields.String,
            "status": fields.String,
            "date": fields.String,
            "type": fields.String,
            "category": fields.String,
            "original_price": fields.Float,
            "discount": fields.Integer,
            "price": fields.Float,
            "code": fields.String,
            "meta": fields.Nested(namespace.model("MetaFilter", {
                    "created_at": fields.String(description="ISO 8601 Date"),
                    "updated_at": fields.String(description="ISO 8601 Date"),
                    "created_by": fields.Integer,
                    "updated_by": fields.Integer,
                }))
        }, ordered=True)

        return namespace.model("ScholarshipFilterResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("ScholarshipFilterData", {
                "list": fields.List(fields.Nested(scholarship_item)),
                "pagination": fields.Nested(namespace.model("ScholarshipPagination", {
                    "current_page": fields.Integer,
                    "page_size": fields.Integer,
                    "total_pages": fields.Integer,
                    "total_items": fields.Integer
                }))
            }))
        }, ordered=True)