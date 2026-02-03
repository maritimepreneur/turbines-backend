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
            }))
        })
    
    @classmethod
    def clock_schema(cls, namespace: Model):
        """Schema for Clock In/Out"""
        return namespace.model("ClockRequest", {
            "timestamp": fields.String(required=False, description="ISO format datetime, default: now"),
            "status": fields.String(required=False, default="On Time", description="On Time / Late / Early"),
            "desc": fields.String(required=False, description="Optional description"),
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

    # --- NEW: Filter & Search Schema ---
    @classmethod
    def filter_schema(cls, namespace: Model):
        """Schema for Payload Search & Filter Attendance"""
        return namespace.model("AttendanceFilterRequest", {
            # Pagination
            "page_size": fields.Integer(required=True, default=10, description="Items per page"),
            "page_number": fields.Integer(required=True, default=1, description="Current page number"),
            
            # Search by Employee Name
            "search": fields.String(description="Search by Employee Name"),
            
            # Filters
            "checked": fields.Boolean(description="Filter by Checked status (true/false)"),
            "start_date": fields.String(description="Filter Start Date (YYYY-MM-DD)"),
            "end_date": fields.String(description="Filter End Date (YYYY-MM-DD)"),
            
            # Sorting
            "sort_order": fields.String(default="DESC", description="ASC or DESC based on Date")
        })

    @classmethod
    def filter_response_schema(cls, namespace: Model):
        """Schema for Output Response Filter (List + Pagination)"""
        
        # Model Item per baris (attendance detail + nama employee)
        attendance_item = namespace.model("AttendanceFilterItem", {
            "id": fields.Integer,
            "date": fields.String,
            "clock_in": fields.Raw,
            "clock_out": fields.Raw,
            "checked": fields.Boolean,
            "employee_id": fields.Integer,
            "employee_name": fields.String(description="Name of the employee"), # Field tambahan hasil Join
        })

        # Model Pagination Info
        pagination_model = namespace.model("AttendancePaginationInfo", {
            "current_page": fields.Integer,
            "page_size": fields.Integer,
            "total_pages": fields.Integer,
            "total_items": fields.Integer
        })

        # Model Data Wrapper
        return namespace.model("AttendanceFilterResponse", {
            "message": fields.String(default="Success"),
            "code": fields.Integer(default=200),
            "status": fields.String(default="success"),
            "data": fields.Nested(namespace.model("AttendanceFilterData", {
                "list": fields.List(fields.Nested(attendance_item)),
                "pagination": fields.Nested(pagination_model)
            }))
        })