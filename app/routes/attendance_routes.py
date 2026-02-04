from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import db
from app.services.attendance_service import AttendanceService
from app.schemas.attendance_schema import AttendanceSchema
from app.utils import role_required

attendance_ns = Namespace("attendances", description="Attendance Management")
attendance_svc = AttendanceService(db.session)

attendance_response_schema = AttendanceSchema.get_schema(attendance_ns)

clock_in_schema = AttendanceSchema.clock_in_schema(attendance_ns)
clock_out_schema = AttendanceSchema.clock_out_schema(attendance_ns)

today_status_schema = AttendanceSchema.today_status_schema(attendance_ns)
attendance_filter_schema = AttendanceSchema.filter_schema(attendance_ns)
attendance_filter_response = AttendanceSchema.filter_response_schema(attendance_ns)

@attendance_ns.route("/")
class AttendanceList(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION") 
    @attendance_ns.doc(security="Bearer Auth")
    @attendance_ns.expect(attendance_filter_schema)
    @attendance_ns.response(200, "Success", attendance_filter_response)
    def post(self):
        """Search and Filter Attendances (Calendar & Status)"""
        return attendance_svc.get_attendance_list_filter(attendance_ns.payload)

@attendance_ns.route("/clock-in")
class ClockIn(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "USER")
    @attendance_ns.doc(security="Bearer Auth")
    @attendance_ns.expect(clock_in_schema)
    @attendance_ns.marshal_with(attendance_response_schema)
    def post(self):
        """Clock in - employee diambil dari token JWT"""
        user_id = get_jwt_identity()
        return attendance_svc.clock_in(user_id, attendance_ns.payload or {})

@attendance_ns.route("/clock-out")
class ClockOut(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "USER")
    @attendance_ns.doc(security="Bearer Auth")
    @attendance_ns.expect(clock_out_schema)
    @attendance_ns.marshal_with(attendance_response_schema)
    def post(self):
        """Clock out - employee diambil dari token JWT"""
        user_id = get_jwt_identity()
        return attendance_svc.clock_out(user_id, attendance_ns.payload or {})

@attendance_ns.route("/status")
class TodayStatus(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "USER")
    @attendance_ns.doc(security="Bearer Auth")
    @attendance_ns.marshal_with(today_status_schema)
    def get(self):
        """Get attendance status hari ini - employee diambil dari token JWT"""
        user_id = get_jwt_identity()
        return attendance_svc.get_today_status(user_id)

@attendance_ns.route("/<int:id>")
class AttendanceDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @attendance_ns.doc(security="Bearer Auth")
    @attendance_ns.marshal_with(attendance_response_schema)
    def get(self, id):
        """Get specific attendance detail"""
        return attendance_svc.get_attendance_by_id(id)
    
    @jwt_required()
    @role_required("ADMIN", "HR")
    @attendance_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """Delete attendance record"""
        return attendance_svc.delete_attendance(id)

@attendance_ns.route("/<int:id>/check")
class ToggleChecked(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR")
    @attendance_ns.doc(security="Bearer Auth")
    @attendance_ns.marshal_with(attendance_response_schema)
    def patch(self, id):
        """Toggle checked status (checked ↔ unchecked)"""
        return attendance_svc.toggle_checked(id)