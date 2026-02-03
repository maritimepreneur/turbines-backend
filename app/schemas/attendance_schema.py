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