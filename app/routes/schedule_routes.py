from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import db
from app.services.schedule_service import ScheduleService
from app.schemas.schedule_schema import ScheduleSchema
from app.utils import role_required

schedule_ns = Namespace("schedules", description="Schedule Management")
schedule_svc = ScheduleService(db.session)

schedule_response_schema = ScheduleSchema.get_schema(schedule_ns)
schedule_post_schema = ScheduleSchema.post_schema(schedule_ns)
schedule_filter_schema = ScheduleSchema.filter_schema(schedule_ns)
schedule_filter_response = ScheduleSchema.filter_response_schema(schedule_ns)
schedule_dropdown_schema = ScheduleSchema.dropdown_list_schema(schedule_ns)

@schedule_ns.route("/employee-list")
class ScheduleEmployeeList(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @schedule_ns.doc(security="Bearer Auth")
    @schedule_ns.marshal_with(schedule_dropdown_schema)
    def get(self):
        """Get list of employees (ID, Name, Code) for dropdown"""
        return schedule_svc.get_employee_list_dropdown()

@schedule_ns.route("/employee")
class MySchedules(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "USER")
    @schedule_ns.doc(security="Bearer Auth")
    @schedule_ns.marshal_list_with(schedule_response_schema)
    def get(self):
        """Get schedules for logged-in user (employee)"""
        user_id = get_jwt_identity()
        return schedule_svc.get_my_schedules(user_id)

@schedule_ns.route("/")
class ScheduleList(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @schedule_ns.doc(security="Bearer Auth")
    @schedule_ns.marshal_list_with(schedule_response_schema)
    def get(self):
        """Get all schedules (Standard)"""
        return schedule_svc.get_all_schedules()
    
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @schedule_ns.doc(security="Bearer Auth")
    @schedule_ns.expect(schedule_filter_schema)
    @schedule_ns.response(200, "Success", schedule_filter_response)
    def post(self):
        """Search and Filter Schedules with Pagination"""
        return schedule_svc.get_schedule_list_filter(schedule_ns.payload)

@schedule_ns.route("/create")
class ScheduleCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @schedule_ns.doc(security="Bearer Auth")
    @schedule_ns.expect(schedule_post_schema)
    @schedule_ns.marshal_with(schedule_response_schema)
    def post(self):
        """Create a new schedule"""
        return schedule_svc.create_schedule(schedule_ns.payload)

@schedule_ns.route("/<int:id>")
class ScheduleDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION", "USER")
    @schedule_ns.doc(security="Bearer Auth")
    @schedule_ns.marshal_with(schedule_response_schema)
    def get(self, id):
        """Get schedule detail"""
        return schedule_svc.get_schedule_by_id(id)
    
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @schedule_ns.doc(security="Bearer Auth")
    @schedule_ns.expect(schedule_post_schema)
    @schedule_ns.marshal_with(schedule_response_schema)
    def put(self, id):
        """Update schedule detail"""
        return schedule_svc.update_schedule(id, schedule_ns.payload)
    
    @jwt_required()
    @role_required("ADMIN", "HR")
    @schedule_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """Delete a schedule"""
        return schedule_svc.delete_schedule(id)