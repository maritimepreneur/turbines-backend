from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class DocumentSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """Schema untuk Detail Document (Single Object)"""
        return namespace.model("DocumentResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Document", {
                "id": fields.Integer,
                "number": fields.Integer,
                "name": fields.String,
                "document_type": fields.String,
                "project_id": fields.Integer,
                "quotation_id": fields.Integer,
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
        """Schema untuk Create/Update Document"""
        return namespace.model("DocumentPostRequest", {
            "number": fields.Integer(required=True),
            "name": fields.String(required=True),
            "document_type": fields.String(
                required=True, 
                enum=["OTHER", "RECOMENDATION", "PO", "INVOICE", "MOU", "TAX", "REPORT", "CERTIFICATE", "AGREEMENT", "QUOTATION"]
            ),
            "project_id": fields.Integer(required=False),
            "quotation_id": fields.Integer(required=False),
        })

    @classmethod
    def filter_schema(cls, namespace: Model):
        """Schema untuk Request Body Search & Filter Document"""
        return namespace.model("DocumentFilterRequest", {
            "page_size": fields.Integer(required=True, default=25),
            "page_number": fields.Integer(required=True, default=1),
            "sort_by": fields.String(required=True, default="id"),
            "sort_order": fields.String(required=True, default="DESC"),
            "search": fields.String(description="Search by Document Name"),
            "document_types": fields.List(fields.String, description="Filter by Document Types (e.g. MOU, PO)"),
            "project_ids": fields.List(fields.Integer, description="Filter by multiple Project IDs"),
            "quotation_ids": fields.List(fields.Integer, description="Filter by multiple Quotation IDs")
        }, ordered=True)

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema untuk Response List Document dengan Pagination"""
        doc_item_model = namespace.model("DocumentFilterItem", {
            "id": fields.Integer,
            "number": fields.Integer,
            "name": fields.String,
            "document_type": fields.String,
            "project_name": fields.String,
            "quotation_summary": fields.String
        }, ordered=True)

        pagination_model = namespace.model("DocPaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        }, ordered=True)

        return namespace.model("DocumentFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(namespace.model("DocFilterData", {
                "list": fields.List(fields.Nested(doc_item_model)),
                "pagination": fields.Nested(pagination_model)
            }))
        }, ordered=True)

    @classmethod
    def list_response_schema(cls, namespace: Model):
        """Schema untuk Response List Biasa (Tanpa Pagination)"""
        document_list_item = namespace.model("DocumentListItem", {
            "id": fields.Integer,
            "number": fields.Integer,
            "name": fields.String,
            "document_type": fields.String,
            "project_id": fields.Integer,
            "quotation_id": fields.Integer,
            "meta": fields.Nested(namespace.model("Meta", {
                    "created_at": fields.String(description="ISO 8601 Date"),
                    "updated_at": fields.String(description="ISO 8601 Date"),
                    "created_by": fields.Integer,
                    "updated_by": fields.Integer,
                })),
        })

        return namespace.model("DocumentListResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.List(fields.Nested(document_list_item))
        })