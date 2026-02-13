from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class ScheduleSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """Schema for Schedule Details"""
        
        # Employee detail model
        employee_detail = namespace.model("ScheduleEmployeeDetail", {
            "id": fields.Integer,
            "full_name": fields.String,
            "employee_code": fields.String,
            "email": fields.String
        })
        
        # Tagged employee model
        tagged_employee = namespace.model("ScheduleTaggedEmployee", {
            "id": fields.Integer,
            "full_name": fields.String,
            "employee_code": fields.String
        })
        
        return namespace.model("ScheduleResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Schedule", {
                "id": fields.Integer,
                "title": fields.String,
                "description": fields.String,
                "start_time": fields.String,
                "end_time": fields.String,
                "date": fields.String,
                "tagged_ids": fields.Raw,
                "employee_id": fields.Integer,
                "employee": fields.Nested(employee_detail, allow_null=True),
                "tagged_employees": fields.List(fields.Nested(tagged_employee))
            }))
        })
    
    @classmethod
    def post_schema(cls, namespace: Model):
        """Schema for Create/Update Schedule"""
        return namespace.model("SchedulePostRequest", {
            "title": fields.String(required=True),
            "description": fields.String(required=True),
            "start_time": fields.String(required=True, description="HH:MM:SS"),
            "end_time": fields.String(required=True, description="HH:MM:SS"),
            "date": fields.String(required=True, description="YYYY-MM-DD or ISO datetime"),
            "tagged_ids": fields.List(fields.Integer, required=False, default=[]),
            "employee_id": fields.Integer(required=True),
        })

    @classmethod
    def filter_schema(cls, namespace: Model):
        """Schema for Payload Request Search & Filter Schedule"""
        return namespace.model("ScheduleFilterRequest", {
            "page_size": fields.Integer(required=True, default=25),
            "page_number": fields.Integer(required=True, default=1),
            "sort_by": fields.String(required=True, default="date"),
            "sort_order": fields.String(required=True, default="DESC"),
            
            "search": fields.String(description="Search by Title, Description, or Employee Name"),
            
            "date_start": fields.String(description="Start Date (YYYY-MM-DD)"),
            "date_end": fields.String(description="End Date (YYYY-MM-DD)"),
            
            "employees": fields.List(fields.String, description="Filter by Employee Names"),
        })

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema for Output Response Filter (List + Pagination)"""
        
        # Employee detail for filter
        employee_detail = namespace.model("ScheduleFilterEmployeeDetail", {
            "id": fields.Integer,
            "full_name": fields.String,
            "employee_code": fields.String,
            "email": fields.String
        })
        
        # Tagged employee for filter
        tagged_employee = namespace.model("ScheduleFilterTaggedEmployee", {
            "id": fields.Integer,
            "full_name": fields.String,
            "employee_code": fields.String
        })
        
        schedule_item_model = namespace.model("ScheduleFilterItem", {
            "id": fields.Integer,
            "title": fields.String,
            "description": fields.String,
            "start_time": fields.String,
            "end_time": fields.String,
            "date": fields.String,
            "tagged_ids": fields.Raw,
            "employee_id": fields.Integer,
            "employee": fields.Nested(employee_detail, allow_null=True),
            "tagged_employees": fields.List(fields.Nested(tagged_employee))
        })

        pagination_model = namespace.model("SchedulePaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        })

        filter_data_model = namespace.model("ScheduleFilterData", {
            "list": fields.List(fields.Nested(schedule_item_model)),
            "pagination": fields.Nested(pagination_model)
        })

        return namespace.model("ScheduleFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(filter_data_model)
        })

    @classmethod
    def dropdown_list_schema(cls, namespace: Model):
        """Schema for Employee Dropdown List"""
        dropdown_item = namespace.model("ScheduleEmployeeDropdownItem", {
            "id": fields.Integer,
            "name": fields.String,
            "code": fields.String
        })

        return namespace.model("ScheduleEmployeeDropdownListResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.List(fields.Nested(dropdown_item))
        })