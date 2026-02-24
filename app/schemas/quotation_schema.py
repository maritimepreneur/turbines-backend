from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class QuotationSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        return namespace.model("QuotationResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Quotation", {
                "id": fields.Integer,
                "total_amount": fields.String(
                    description="Decimal/Numeric amount as string, example 15000.00",
                    required=True
                ),
                "document_content": fields.String,
                "summary": fields.String,
                "offering_letter": fields.String,
                "contact": fields.Nested(namespace.model("QuotationContact", {
                    "id": fields.Integer,
                    "name": fields.String,
                    "company": fields.String,
                })),
                "partner": fields.Nested(namespace.model("QuotationPartner", {
                    "id": fields.Integer,
                    "name": fields.String,
                    "service": fields.String,
                    "goods": fields.String,
                })),
                "lead": fields.Nested(namespace.model("QuotationLead", {
                    "id": fields.Integer,
                    "name": fields.String,
                    "period": fields.String,
                    "current_stages": fields.String,
                })),
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
        return namespace.model("QuotationPostResponse", {
            "total_amount": fields.String(
                description="Decimal/Numeric amount as string, example 15000.00",
                required=True
            ),
            "document_content": fields.String(required=True),
            "summary": fields.String(required=True),
            "offering_letter": fields.String(required=True),
            "contact_id": fields.Integer(required=False, allow_null=True),
            "partner_id": fields.Integer(required=False, allow_null=True),
            "lead_id": fields.Integer(required=False, allow_null=True),
        })

    @classmethod
    def filter_schema(cls, namespace: Model):
        """Schema untuk Request Body Search & Filter Quotation"""
        return namespace.model("QuotationFilterRequest", {
            "page_size": fields.Integer(required=True, default=25),
            "page_number": fields.Integer(required=True, default=1),
            "sort_by": fields.String(required=True, default="id"),
            "sort_order": fields.String(required=True, default="DESC"),
            "search": fields.String(description="Search by Summary, Partner Name, or Lead Name"),
            "min_amount": fields.Float(description="Minimum total amount"),
            "max_amount": fields.Float(description="Maximum total amount"),
            "partner_ids": fields.List(fields.Integer, description="Filter by Partner IDs")
        }, ordered=True)

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema untuk Response List Quotation dengan Pagination"""
        quotation_item = namespace.model("QuotationFilterItem", {
            "id": fields.Integer,
            "total_amount": fields.String,
            "summary": fields.String,
            "contact_name": fields.String,
            "partner_name": fields.String,
            "lead_name": fields.String,
            "created_at": fields.String
        }, ordered=True)

        pagination = namespace.model("QuotationPaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        }, ordered=True)

        return namespace.model("QuotationFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(namespace.model("QuotationFilterData", {
                "list": fields.List(fields.Nested(quotation_item)),
                "pagination": fields.Nested(pagination)
            }))
        }, ordered=True)