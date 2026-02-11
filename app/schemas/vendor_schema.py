from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema
from app.models.partners import CompanyType, PartnerType

class VendorSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """Schema untuk single vendor response"""
        return namespace.model("VendorResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Vendor", {
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
        })
    
    @classmethod
    def post_schema(cls, namespace: Model):
        """Schema untuk create vendor"""
        company_type_values = [e.value for e in CompanyType]
        
        return namespace.model("VendorPostRequest", {
            "name": fields.String(required=True),
            "initials": fields.String(required=True),
            "industry": fields.String(required=True),
            "company_type": fields.String(
                required=True,
                enum=company_type_values,
                description=f"Valid values: {company_type_values}"
            ),
            "service": fields.List(fields.String, default=[]),
            "goods": fields.List(fields.String, default=[]),
        })
    
    @classmethod
    def filter_schema(cls, namespace: Model):
        """Schema untuk filter vendors - TAMBAHKAN METHOD INI"""
        return namespace.model("VendorFilter", {
            "search": fields.String(required=False, description="Search by name or initials"),
            "industry": fields.String(required=False, description="Filter by industry"),
            "company_type": fields.String(
                required=False, 
                enum=[e.value for e in CompanyType],
                description="Filter by company type"
            ),
            "page": fields.Integer(required=False, default=1, description="Page number"),
            "per_page": fields.Integer(required=False, default=10, description="Items per page"),
            "sort_by": fields.String(
                required=False, 
                default="created_at",
                enum=["name", "industry", "company_type", "created_at"],
                description="Field to sort by"
            ),
            "sort_order": fields.String(
                required=False,
                default="desc",
                enum=["asc", "desc"],
                description="Sort order"
            )
        })
    
    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema untuk response filtered vendors dengan pagination - TAMBAHKAN METHOD INI"""
        return namespace.model("VendorFilterResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.List(fields.Nested(namespace.model("VendorItem", {
                "id": fields.Integer,
                "name": fields.String,
                "initials": fields.String,
                "industry": fields.String,
                "company_type": fields.String,
                "partner_type": fields.String,
                "created_at": fields.String
            }))),
            "pagination": fields.Nested(namespace.model("VendorPagination", {
                "page": fields.Integer,
                "per_page": fields.Integer,
                "total": fields.Integer,
                "pages": fields.Integer,
                "has_next": fields.Boolean,
                "has_prev": fields.Boolean
            }), skip_none=True)
        })
    
    @classmethod
    def list_schema(cls, namespace: Model):
        """Schema untuk get all vendors (simple list)"""
        return namespace.model("VendorListResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.List(fields.Nested(namespace.model("VendorSimpleItem", {
                "id": fields.Integer,
                "name": fields.String,
                "initials": fields.String,
                "industry": fields.String,
                "company_type": fields.String,
                "partner_type": fields.String
            })))
        })