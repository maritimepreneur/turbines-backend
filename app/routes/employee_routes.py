from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.employee_service import EmployeeService
from app.schemas.employee_schema import EmployeeSchema
from app.utils import role_required

employee_ns = Namespace("employees", description="Employee Management")
employee_svc = EmployeeService(db.session)

employee_response_schema = EmployeeSchema.get_schema(employee_ns)
employee_post_schema = EmployeeSchema.post_schema(employee_ns)
employee_filter_schema = EmployeeSchema.filter_schema(employee_ns)
employee_filter_response = EmployeeSchema.filter_response_schema(employee_ns)
employee_list_response = EmployeeSchema.list_response_schema(employee_ns)


@employee_ns.route("/")
class EmployeeList(Resource):

    @jwt_required()
    @role_required("ADMIN", "HR")
    @employee_ns.doc(security="Bearer Auth")
    @employee_ns.response(200, "Success Retrieve All Data", employee_list_response)
    def get(self):
        """ Ambil semua data karyawan """
        return employee_svc.get_all_employees()

    @jwt_required()
    @role_required("ADMIN", "HR")
    @employee_ns.doc(security="Bearer Auth")
    @employee_ns.expect(employee_filter_schema)
    @employee_ns.response(200, "Success", employee_filter_response)
    def post(self):
        """ Cari dan Filter karyawan dengan pagination """
        return employee_svc.get_employee_list_filter(employee_ns.payload)


@employee_ns.route("/create")
class EmployeeCreate(Resource):

    @jwt_required()
    @employee_ns.doc(security="Bearer Auth")
    @employee_ns.expect(employee_post_schema)
    @employee_ns.marshal_with(employee_response_schema)
    def post(self):
        """ Membuat data karyawan baru (Otomatis ambil user login) """
        return employee_svc.create_employee(employee_ns.payload)

@employee_ns.route("/profile")
class EmployeeProfile(Resource):
    
    @jwt_required()
    @role_required("ADMIN", "HR", "USER")
    @employee_ns.doc(security="Bearer Auth")
    @employee_ns.marshal_with(employee_response_schema)
    def get(self):
        """ Get My Profile (berdasarkan Token Login) """
        return employee_svc.get_current_employee_profile()


@employee_ns.route("/<int:id>")
class EmployeeDetail(Resource):

    @jwt_required()
    @role_required("ADMIN", "HR", "USER")
    @employee_ns.doc(security="Bearer Auth")
    @employee_ns.marshal_with(employee_response_schema)
    def get(self, id):
        """ Ambil detail karyawan berdasarkan ID """
        return employee_svc.get_employee_by_id(id)

    @jwt_required()
    @employee_ns.doc(security="Bearer Auth")
    @employee_ns.expect(employee_post_schema)
    @employee_ns.marshal_with(employee_response_schema)
    def put(self, id):
        """ Update data detail karyawan """
        return employee_svc.update(id, employee_ns.payload)

    @jwt_required()
    @role_required("ADMIN")
    @employee_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Menghapus data karyawan """
        return employee_svc.delete(id)