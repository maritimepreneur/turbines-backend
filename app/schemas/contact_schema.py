from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class ContactSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """ Schema untuk menampilkan detail Contact (Standard) """
        return namespace.model("ContactResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Contact", {
                "id": fields.Integer,
                "name": fields.String,
                "emails": fields.List(fields.String),
                "phone_numbers": fields.List(fields.String),
                "company": fields.String,
                "partner_id": fields.Integer(required=False, allow_null=True),
                "created_at": fields.String(description="ISO 8601 Date")
            }))
        })
    
    @classmethod
    def post_schema(cls, namespace: Model):
        """ Schema untuk Create/Update Contact """
        return namespace.model("ContactPostRequest", {
            "name": fields.String(required=True),
            "emails": fields.List(fields.String, required=True),
            "phone_numbers": fields.List(fields.String ,required=True),
            "company": fields.String,
            "partner_id": fields.Integer(description="Optional Partner ID", required=False, allow_null=True)
        })

    @classmethod
    def filter_schema(cls, namespace: Model):
        """ Schema untuk Payload Request Search & Filter """
        return namespace.model("ContactFilterRequest", {
            "page_size": fields.Integer(required=True, default=25, description="Items per page"),
            "page_number": fields.Integer(required=True, default=1, description="Current page number"),
            "sort_by": fields.String(required=True, default="id", description="Field to sort by"),
            "sort_order": fields.String(required=True, default="DESC", description="ASC or DESC"),
            "search": fields.String(description="Global search by Name or Emails"),
            "names": fields.List(fields.String, description="Filter by List of Names (Partial Match)"),
            "companies": fields.List(fields.String, description="Filter by List of Companies (Partial Match)"),
            "emails": fields.List(fields.String, description="Filter by List of Emails"),
            "phone_numbers": fields.List(fields.String, description="Filter by List of Phone Numbers"),
            "start_date": fields.String(description="Start Date (YYYY-MM-DD)"),
            "end_date": fields.String(description="End Date (YYYY-MM-DD)"),
        })

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """ Schema untuk Output Response Filter (List + Pagination) """
        
        contact_item_model = namespace.model("ContactFilterItem", {
            "id": fields.Integer,
            "name": fields.String,
            "emails": fields.List(fields.String),
            "phone_numbers": fields.List(fields.String),
            "company": fields.String,
            "partner_id": fields.Integer,
            "created_at": fields.String
        })

        pagination_model = namespace.model("ContactPaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        })

        filter_data_model = namespace.model("ContactFilterData", {
            "list": fields.List(fields.Nested(contact_item_model)),
            "pagination": fields.Nested(pagination_model)
        })

        return namespace.model("ContactFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(filter_data_model)
        })