from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class PartnerSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("PartnerResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Partner", {
                "id": fields.Integer,
                "name": fields.String,
                "initials": fields.String,
                "industrials": fields.String(attribute="industry"), # Mapping ke field model 'industry'
                "company_type": fields.String(
                    attribute=lambda x: x.company_type.value if x and x.company_type else None
                ),
                "partner_type": fields.String(
                    attribute=lambda x: x.partner_type.value if x and x.partner_type else None
                ),
                "service": fields.String,
                "goods": fields.String,
            }))
        })
    
    @classmethod
    def post_schema(cls, namespace: Model):
        return namespace.model("PartnerPostResponse", {
            "name": fields.String(required=True),
            "initials": fields.String(required=True),
            "industry": fields.String(required=True),
            "company_type": fields.String(required=True),
            "partner_type": fields.String(required=True),
            "service": fields.String,
            "goods": fields.String,
        })

    @classmethod
    def filter_schema(cls, namespace: Model):
        """ Schema untuk Payload Request Search & Filter Partner """
        return namespace.model("PartnerFilterRequest", {

            "page_size": fields.Integer(required=True, default=25),
            "page_number": fields.Integer(required=True, default=1),
            "sort_by": fields.String(required=True, default="id"),
            "sort_order": fields.String(required=True, default="DESC"),
            
            "search": fields.String(description="Search by Name or Initials"),
            
            "industries": fields.List(fields.String, description="Filter by Industry (Partial Match)"),
            "company_types": fields.List(fields.String, description="Filter by Company Type (Exact Match e.g., 'Private')"),
            "partner_types": fields.List(fields.String, description="Filter by Partner Type (Exact Match e.g., 'Vendor')"),
            "services": fields.List(fields.String, description="Filter by Service (Partial Match)"),
            "goods": fields.List(fields.String, description="Filter by Goods (Partial Match)"),
        })

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """ Schema untuk Output Response Filter (List + Pagination) """
        
        partner_item_model = namespace.model("PartnerFilterItem", {
            "id": fields.Integer,
            "name": fields.String,
            "initials": fields.String,
            "industry": fields.String,
            "company_type": fields.String,
            "partner_type": fields.String,
            "service": fields.String,
            "goods": fields.String,
            "created_at": fields.String
        })

        pagination_model = namespace.model("PartnerPaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        })

        filter_data_model = namespace.model("PartnerFilterData", {
            "list": fields.List(fields.Nested(partner_item_model)),
            "pagination": fields.Nested(pagination_model)
        })

        return namespace.model("PartnerFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(filter_data_model)
        })