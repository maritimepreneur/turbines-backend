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