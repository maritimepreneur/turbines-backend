from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class QuotationSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        approval_model = namespace.model("ExpenseApproval", {
            "id": fields.Integer,
            "code": fields.String,
            "type": fields.String,
        })

        expense_model = namespace.model("ItemExpense", {
            "id": fields.Integer,
            "code": fields.String,
            "total_amount": fields.Float,
            "status": fields.String(attribute=lambda x: x.status.value if x.status else None),

            # nested approval
            "approval": fields.Nested(approval_model),
        })
        
        item_model = namespace.model("QuotationItem", {
            "id": fields.Integer,
            "name": fields.String,
            "cost": fields.Float,
            "amount": fields.Float,
            "billed_amount": fields.Float,
            "type": fields.String(attribute=lambda x: x.type.value if x.type else None),
            "amount_type": fields.String,
            "code": fields.String,
            "attachments": fields.Raw,

            "expense": fields.Nested(expense_model),
        })

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
                "items": fields.List(fields.Nested(item_model), attribute="items"),
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
        item_model = namespace.model("QuotationItemInput", {
            "name": fields.String(required=True),
            "cost": fields.Float(required=True),
            "amount": fields.Float(required=True),
            "billed_amount": fields.Float(required=True),
            "type": fields.String(required=True),
            "amount_type": fields.String(required=True),
            "attachments": fields.Raw,
        })

        return namespace.model("QuotationPostResponse", {
            "total_amount": fields.String(required=True),
            "document_content": fields.String(required=True),
            "summary": fields.String(required=True),
            "offering_letter": fields.String(required=True),
            "contact_id": fields.Integer,
            "partner_id": fields.Integer,
            "lead_id": fields.Integer,

            "items": fields.List(fields.Nested(item_model))
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