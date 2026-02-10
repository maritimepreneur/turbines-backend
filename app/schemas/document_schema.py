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
        """Schema untuk Request Filter"""
        return namespace.model("DocumentFilterRequest", {
            "search": fields.String(description="Cari berdasarkan nama"),
            "document_types": fields.List(fields.String, description="Filter tipe (List of String)"),
            "project_id": fields.Integer(),
            "page_number": fields.Integer(default=1),
            "page_size": fields.Integer(default=25),
            "sort_by": fields.String(default="id"),
            "sort_order": fields.String(default="DESC")
        })

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema untuk Response dengan Pagination"""
        pagination_model = namespace.model("DocPagination", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        })
        
        doc_item = namespace.model("DocItem", {
            "id": fields.Integer,
            "number": fields.Integer,
            "name": fields.String,
            "document_type": fields.String
        })

        return namespace.model("DocumentFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(namespace.model("DocFilterData", {
                "list": fields.List(fields.Nested(doc_item)),
                "pagination": fields.Nested(pagination_model)
            }))
        })

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
        })

        return namespace.model("DocumentListResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.List(fields.Nested(document_list_item))
        })