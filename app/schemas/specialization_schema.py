from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class SpecializationSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """Schema for Specialization Details"""
        meta_model = namespace.model("SpecializationMeta", {
            "created_at": fields.String,
            "updated_at": fields.String,
            "created_by": fields.String,
            "updated_by": fields.String
        })
        
        return namespace.model("SpecializationResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Specialization", {
                "id": fields.Integer,
                "name": fields.String,
                "description": fields.String,
                "code": fields.String,
                "meta": fields.Nested(meta_model)
            }))
        })
    
    @classmethod
    def post_schema(cls, namespace: Model):
        """Schema for Create/Update Specialization"""
        return namespace.model("SpecializationPostRequest", {
            "name": fields.String(required=True, description="Specialization name"),
            "description": fields.String(required=True, description="Specialization description"),
            "code": fields.String(required=True, description="Unique specialization code"),
        })

    @classmethod
    def filter_schema(cls, namespace: Model):
        """Schema for Payload Request Search & Filter Specialization"""
        return namespace.model("SpecializationFilterRequest", {
            "page_size": fields.Integer(required=True, default=25),
            "page_number": fields.Integer(required=True, default=1),
            "sort_by": fields.String(required=True, default="id"),
            "sort_order": fields.String(required=True, default="DESC"),
            
            "search": fields.String(description="Search by Name, Code, or Description"),
        })

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema for Output Response Filter (List + Pagination)"""
        
        meta_model = namespace.model("SpecializationFilterMeta", {
            "created_at": fields.String,
            "updated_at": fields.String,
            "created_by": fields.String,
            "updated_by": fields.String
        })
        
        specialization_item_model = namespace.model("SpecializationFilterItem", {
            "id": fields.Integer,
            "name": fields.String,
            "description": fields.String,
            "code": fields.String,
            "meta": fields.Nested(meta_model)
        })

        pagination_model = namespace.model("SpecializationPaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        })

        filter_data_model = namespace.model("SpecializationFilterData", {
            "list": fields.List(fields.Nested(specialization_item_model)),
            "pagination": fields.Nested(pagination_model)
        })

        return namespace.model("SpecializationFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(filter_data_model)
        })