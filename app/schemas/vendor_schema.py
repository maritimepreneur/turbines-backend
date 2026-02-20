from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema
from app.models.partners import CompanyType

class VendorSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """Schema untuk single vendor response"""
        return namespace.model("VendorResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("VendorDetail", {
                "id": fields.Integer,
                "name": fields.String,
                "initials": fields.String,
                "industry": fields.String,
                "company_type": fields.String,
                "partner_type": fields.String,
                "service": fields.List(fields.String),
                "goods": fields.List(fields.String),
                "created_at": fields.String
            }))
        }, ordered=True)

    @classmethod
    def filter_schema(cls, namespace: Model):
        """Schema untuk Request Body Search & Filter"""
        return namespace.model("VendorFilterRequest", {
            "page_size": fields.Integer(required=True, default=25),
            "page_number": fields.Integer(required=True, default=1),
            "sort_by": fields.String(required=True, default="id"),
            "sort_order": fields.String(required=True, default="DESC"),
            "search": fields.String(description="Search by Name, Initials, or Industry"),
            "company_types": fields.List(fields.String, description="Filter by Company Types (e.g. PRIVATE, GOVERMENT)"),
            "industries": fields.List(fields.String, description="Filter by Industry names")
        }, ordered=True)

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema untuk Response List dengan Pagination"""
        vendor_item = namespace.model("VendorFilterItem", {
            "id": fields.Integer,
            "name": fields.String,
            "initials": fields.String,
            "industry": fields.String,
            "company_type": fields.String,
            "partner_type": fields.String,
            "created_at": fields.String
        }, ordered=True)

        pagination = namespace.model("VendorPaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        }, ordered=True)

        return namespace.model("VendorFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(namespace.model("VendorFilterData", {
                "list": fields.List(fields.Nested(vendor_item)),
                "pagination": fields.Nested(pagination)
            }))
        }, ordered=True)

    @classmethod
    def post_schema(cls, namespace: Model):
        """Schema untuk Create/Update Vendor"""
        return namespace.model("VendorPostRequest", {
            "name": fields.String(required=True),
            "initials": fields.String(required=True),
            "industry": fields.String(required=True),
            "company_type": fields.String(required=True, enum=[e.value for e in CompanyType]),
            "service": fields.List(fields.String, default=[]),
            "goods": fields.List(fields.String, default=[]),
        }, ordered=True)