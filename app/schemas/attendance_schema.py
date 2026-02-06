from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class AttendanceSchema(BaseSchema):
    @classmethod
    def get_schema(cls, namespace: Model):
        """Schema for Attendance Details"""
        return namespace.model("AttendanceResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("Attendance", {
                "id": fields.Integer,
                "date": fields.String,
                "clock_in": fields.Raw,
                "clock_out": fields.Raw,
                "checked": fields.Boolean,
                "employee_id": fields.Integer,
                "employee_name": fields.String(description="Name of the employee"),
            }))
        })
    
    @classmethod
    def clock_in_schema(cls, namespace: Model):
        """Schema for Clock In Request (No Desc)"""
        return namespace.model("ClockInRequest", {
            "status": fields.String(required=False, default="On Time", description="On Time / Late / Early"),
            "latitude": fields.Float(required=False),
            "longitude": fields.Float(required=False),
        })

    @classmethod
    def clock_out_schema(cls, namespace: Model):
        """Schema for Clock Out Request (With Desc)"""
        return namespace.model("ClockOutRequest", {
            "status": fields.String(required=False, default="On Time", description="On Time / Late / Early"),
            "desc": fields.String(required=False, description="Work description"),
            "latitude": fields.Float(required=False),
            "longitude": fields.Float(required=False),
        })

    @classmethod
    def today_status_schema(cls, namespace: Model):
        """Schema for Today Status Response"""
        return namespace.model("TodayStatusResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(namespace.model("TodayStatus", {
                "clocked_in": fields.Boolean,
                "clocked_out": fields.Boolean,
                "attendance": fields.Raw(allow_null=True)
            }))
        })

    @classmethod
    def filter_schema(cls, namespace: Model):
        """Schema for Payload Search & Filter Attendance"""
        return namespace.model("AttendanceFilterRequest", {
            "page_size": fields.Integer(required=True, default=10),
            "page_number": fields.Integer(required=True, default=1),
            "search": fields.String(description="Search by Employee Name"),
            "checked": fields.Boolean(description="Filter by Checked status"),
            "start_date": fields.String(description="Filter Start Date (YYYY-MM-DD)"),
            "end_date": fields.String(description="Filter End Date (YYYY-MM-DD)"),
            "sort_order": fields.String(default="DESC")
        })

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema for Output Response Filter"""
        attendance_item = namespace.model("AttendanceFilterItem", {
            "id": fields.Integer,
            "date": fields.String,
            "clock_in": fields.Raw,
            "clock_out": fields.Raw,
            "checked": fields.Boolean,
            "employee_id": fields.Integer,
            "employee_name": fields.String,
        })

        pagination_model = namespace.model("AttendancePaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        })

        return namespace.model("AttendanceFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(namespace.model("AttendanceFilterData", {
                "list": fields.List(fields.Nested(attendance_item)),
                "pagination": fields.Nested(pagination_model)
            }))
        })

    @classmethod
    def absent_list_response_schema(cls, namespace: Model):
        """Schema untuk Response Absent List"""
        
        absent_item = namespace.model("AbsentEmployeeItem", {
            "id": fields.Integer, 
            "employee_name": fields.String,
            "employee_code": fields.String,
            "job_title": fields.String(attribute="nickname"),
            "img_url": fields.String,
            "phone": fields.String
        })

        return namespace.model("AbsentListResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.List(fields.Nested(absent_item))
        })