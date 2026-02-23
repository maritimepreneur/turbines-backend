from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class EmployeeSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """Schema untuk Detail Employee (Single Object)"""
        return namespace.model("EmployeeResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Employee", {
                "id": fields.Integer,
                "full_name": fields.String,
                "nickname": fields.String,
                "residence_address": fields.String,
                "permanent_address": fields.String,
                "birth_place": fields.String,
                "birth_date": fields.String,
                "religion": fields.String,
                "blood_type": fields.String,
                "nationality": fields.String,
                "marital_status": fields.String,
                "ktp": fields.String,
                "driving_license": fields.String,
                "npwp": fields.String,
                "phone": fields.String,
                "whatsapp": fields.String,
                "email": fields.String,
                "handphone": fields.String,
                "employee_code": fields.String,
                "img_url": fields.String,
                "signature_img_url": fields.String,
                "signature_scale": fields.Float,
                "user_id": fields.Integer,
            }))
        })

    @classmethod
    def post_schema(cls, namespace: Model):
        """Schema untuk Create/Update Employee"""
        return namespace.model("EmployeePostRequest", {
            "full_name": fields.String(required=True),
            "nickname": fields.String(required=True),
            "residence_address": fields.String(required=True),
            "permanent_address": fields.String(required=True),
            "birth_place": fields.String(required=True),
            "birth_date": fields.Date(required=True, description="Format: YYYY-MM-DD"),
            "religion": fields.String(required=True, enum=["ISLAM", "CHRISTIANITY", "HINDUISM", "BUDDHISM", "CONFUCIANISM", "OTHER"]),
            "blood_type": fields.String(required=True, enum=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]),
            "nationality": fields.String(required=True),
            "marital_status": fields.String(required=True, enum=["SINGLE", "MARRIED", "WIDOWED", "DIVORCED", "SEPARATED"]),
            "ktp": fields.String(required=True),
            "driving_license": fields.String(required=True),
            "npwp": fields.String(required=True),
            "phone": fields.String(required=True),
            "whatsapp": fields.String(required=True),
            "email": fields.String(required=True),
            "handphone": fields.String(required=True),
            "employee_code": fields.String(readonly=True, description="Auto-generated (EMP-XXXX)"),
            "img_url": fields.String,
            "signature_img_url": fields.String,
            "signature_scale": fields.Float(default=1.0),
        })

    @classmethod
    def filter_schema(cls, namespace: Model):
        """Schema untuk Payload Filter & Search"""
        return namespace.model("EmployeeFilterRequest", {
            "page_size": fields.Integer(default=25),
            "page_number": fields.Integer(default=1),
            "sort_by": fields.String(default="id"),
            "sort_order": fields.String(default="DESC"),
            "search": fields.String(description="Search by Name, Nickname, or Code"),
            "religions": fields.List(fields.String),
            "blood_types": fields.List(fields.String),
            "marital_statuses": fields.List(fields.String),
        })

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema untuk Response List dengan Pagination"""
        employee_item_model = namespace.model("EmployeeFilterItem", {
            "id": fields.Integer,
            "employee_code": fields.String,
            "full_name": fields.String,
            "nickname": fields.String,
            "email": fields.String,
            "phone": fields.String,
            "img_url": fields.String,
        })

        pagination_model = namespace.model("EmployeePaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        })

        return namespace.model("EmployeeFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(namespace.model("EmployeeFilterData", {
                "list": fields.List(fields.Nested(employee_item_model)),
                "pagination": fields.Nested(pagination_model)
            }))
        })

    @classmethod
    def list_response_schema(cls, namespace: Model):
        """Schema untuk Response Get All (Array of Objects)"""
        employee_list_item = namespace.model("EmployeeListItem", {
            "id": fields.Integer,
            "full_name": fields.String,
            "nickname": fields.String,
            "employee_code": fields.String,
            "email": fields.String,
            "phone": fields.String,
            "img_url": fields.String,
            "religion": fields.String,
        })

        return namespace.model("EmployeeListResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.List(fields.Nested(employee_list_item))
        })