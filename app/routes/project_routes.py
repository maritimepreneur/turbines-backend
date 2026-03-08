from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.project_service import ProjectService
from app.schemas.project_schema import ProjectSchema
from app.utils import role_required

project_ns = Namespace("projects", description="Project Management")
project_svc = ProjectService(db.session)
project_response_schema = ProjectSchema.get_schema(project_ns)
project_post_schema = ProjectSchema.post_schema(project_ns)
project_filter_schema = ProjectSchema.filter_schema(project_ns)
project_filter_response = ProjectSchema.filter_response_schema(project_ns)

@project_ns.route("/")
class ProjectList(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "OPERATION")
    @project_ns.doc(security="Bearer Auth")
    @project_ns.expect(project_filter_schema)
    @project_ns.response(200, "Success", project_filter_response)
    def post(self):
        """ Search and Filter Projects with Pagination """
        return project_svc.get_project_list_filter(project_ns.payload)

    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "OPERATION")
    @project_ns.doc(security="Bearer Auth")
    @project_ns.response(200, "Success", project_response_schema)
    def get(self):
        """ Get all projects (Simple List) """
        return project_svc.get_all_projects()
    
@project_ns.route("/create")
class ProjectCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "OPERATION")
    @project_ns.doc(security="Bearer Auth")
    @project_ns.expect(project_post_schema)
    @project_ns.marshal_with(project_response_schema)
    def post(self):
        """ Create a new project """
        return project_svc.create_project(project_ns.payload)
    
@project_ns.route("/<int:id>")
class ProjectDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "OPERATION", "USER")
    @project_ns.doc(security="Bearer Auth")
    @project_ns.marshal_with(project_response_schema)
    def get(self, id):
        """ Get detail project """
        return project_svc.get_project_by_id(id)
    
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "OPERATION")
    @project_ns.doc(security="Bearer Auth")
    @project_ns.expect(project_post_schema)
    @project_ns.marshal_with(project_response_schema)
    def put(self, id):
        """ Update project detail """
        return project_svc.update_project_by_id(id, project_ns.payload)
    
    @jwt_required()
    @role_required("ADMIN")
    @project_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Delete a project """
        return project_svc.delete(id)