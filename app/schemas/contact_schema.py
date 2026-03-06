from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class ContactSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """ Schema untuk menampilkan detail Contact (Standard) """

        partner_model = namespace.model("ContactPartnerDetail", {
            "id": fields.Integer,
            "name": fields.String,
            "initials": fields.String,
            "industry": fields.String,
            "company_type": fields.String,
            "partner_type": fields.String,
            "service": fields.Raw,
            "goods": fields.Raw,
        })

        return namespace.model("ContactResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Contact", {
                "id": fields.Integer,
                "name": fields.String,
                "emails": fields.List(fields.String),
                "phone_numbers": fields.List(fields.String),
                "company": fields.String,
                "role": fields.String(description="Role of the contact"),
                "position": fields.String(description="Position of the contact"),
                "partner_id": fields.Integer(required=False, allow_null=True),
                "partner": fields.Nested(partner_model, allow_null=True, skip_none=True),
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
        """ Schema untuk Create/Update Contact """
        return namespace.model("ContactPostRequest", {
            "name": fields.String(required=True),
            "emails": fields.List(fields.String, required=True),
            "phone_numbers": fields.List(fields.String, required=True),
            "company": fields.String,
            "role": fields.String(description="Role of the contact", required=False),
            "position": fields.String(description="Position of the contact", required=False),
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

        partner_inline_model = namespace.model("ContactFilterPartnerDetail", {
            "id": fields.Integer,
            "name": fields.String,
            "initials": fields.String,
            "industry": fields.String,
            "company_type": fields.String,
            "partner_type": fields.String,
            "service": fields.Raw,
            "goods": fields.Raw,
        })

        contact_item_model = namespace.model("ContactFilterItem", {
            "id": fields.Integer,
            "name": fields.String,
            "emails": fields.List(fields.String),
            "phone_numbers": fields.List(fields.String),
            "company": fields.String,
            "role": fields.String,
            "position": fields.String,
            "partner_id": fields.Integer,
            "partner": fields.Nested(partner_inline_model, allow_null=True, skip_none=True),
            "created_at": fields.String,
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