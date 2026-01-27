from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class LeadSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """ Schema for Lead Details """
        return namespace.model("LeadResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Lead", {
                "id": fields.Integer,
                "name": fields.String,
                "period": fields.Date,
                "description": fields.String,
                "contact_id": fields.Integer,
                "partner_id": fields.Integer,
                "contact": fields.Nested(namespace.model("LeadContact", {
                    "id": fields.Integer,
                    "name": fields.String,
                    "company": fields.String,
                }), allow_null=True),
                "partner": fields.Nested(namespace.model("LeadPartner", {
                    "id": fields.Integer,
                    "name": fields.String,
                }), allow_null=True),
            }))
        })
    
    @classmethod
    def post_schema(cls, namespace: Model):
        """ Schema for Create/Update Lead """
        return namespace.model("LeadPostRequest", {
            "name": fields.String(required=True),
            "period": fields.Date(required=True),
            "description": fields.String(required=True),
            "contact_id": fields.Integer(required=False),
            "partner_id": fields.Integer(required=False),
        })

    @classmethod
    def filter_schema(cls, namespace: Model):
        """ Schema for Payload Request Search & Filter Lead """
        return namespace.model("LeadFilterRequest", {
            "page_size": fields.Integer(required=True, default=25),
            "page_number": fields.Integer(required=True, default=1),
            "sort_by": fields.String(required=True, default="id"),
            "sort_order": fields.String(required=True, default="DESC"),
            
            "search": fields.String(description="Search by Lead Name or Company Name"),
            
            "period_start": fields.String(description="Start Date (YYYY-MM-DD)"),
            "period_end": fields.String(description="End Date (YYYY-MM-DD)"),
            
            "contacts": fields.List(fields.String, description="Filter by Contact Names (Partial Match)"),
            "partners": fields.List(fields.String, description="Filter by Partner Names (Partial Match)"),
            "stages": fields.List(fields.String, description="Filter by Stages (NEW, INTRODUCTION, etc)"), 
        })

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """ Schema for Output Response Filter (List + Pagination) """
        
        lead_item_model = namespace.model("LeadFilterItem", {
            "id": fields.Integer,
            "name": fields.String,
            "period": fields.String,
            "description": fields.String,
            "contact_name": fields.String,
            "company": fields.String,
            "partner_name": fields.String
        })

        pagination_model = namespace.model("LeadPaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        })

        filter_data_model = namespace.model("LeadFilterData", {
            "list": fields.List(fields.Nested(lead_item_model)),
            "pagination": fields.Nested(pagination_model)
        })

        return namespace.model("LeadFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(filter_data_model)
        })

    @classmethod
    def dropdown_list_schema(cls, namespace: Model):
        """ Schema for Dropdown List """
        dropdown_item = namespace.model("DropdownItem", {
            "id": fields.Integer,
            "name": fields.String
        })

        return namespace.model("DropdownListResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.List(fields.Nested(dropdown_item))
        })