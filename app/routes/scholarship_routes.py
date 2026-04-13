from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from flask import request

from app.database import db
from app.services.scholarship_services import ScholarshipService
from app.schemas.scholarship_schema import ScholarshipSchema
from app.utils import role_required


scholarship_ns = Namespace("scholarship", description="Scholarship Management")

service = ScholarshipService(db.session)

scholarship_detail_schema = ScholarshipSchema.get_schema(scholarship_ns)
scholarship_post_schema = ScholarshipSchema.post_schema(scholarship_ns)
scholarship_filter_schema = ScholarshipSchema.filter_response_schema(scholarship_ns)


@scholarship_ns.route("/")
class ScholarshipList(Resource):

    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @scholarship_ns.doc(security="Bearer Auth")
    @scholarship_ns.marshal_with(scholarship_filter_schema)
    def get(self):
        """Get all scholarships with search & filter"""

        payload = {
            "page_size": request.args.get("page_size", 10, type=int),
            "page_number": request.args.get("page_number", 1, type=int),
            "search": request.args.get("search"),
            "status": request.args.get("status"),
            "category": request.args.get("category"),
            "sort_by": request.args.get("sort_by", "id"),
            "sort_order": request.args.get("sort_order", "DESC")
        }

        return service.get_all(payload)


@scholarship_ns.route("/create")
class ScholarshipCreate(Resource):

    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @scholarship_ns.doc(security="Bearer Auth")
    @scholarship_ns.expect(scholarship_post_schema)
    @scholarship_ns.marshal_with(scholarship_detail_schema)
    def post(self):
        """Create scholarship"""
        return service.create(scholarship_ns.payload)


@scholarship_ns.route("/<int:id>")
class ScholarshipDetail(Resource):

    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @scholarship_ns.doc(security="Bearer Auth")
    @scholarship_ns.marshal_with(scholarship_detail_schema)
    def get(self, id):
        """Get scholarship detail"""
        return service.get_by_id(id)

    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @scholarship_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """Delete scholarship"""
        return service.delete(id)


@scholarship_ns.route("/update/<int:id>")
class ScholarshipUpdate(Resource):

    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @scholarship_ns.doc(security="Bearer Auth")
    @scholarship_ns.expect(ScholarshipSchema.update_schema(scholarship_ns)) 
    @scholarship_ns.marshal_with(ScholarshipSchema.get_schema(scholarship_ns))
    def put(self, id):
        """Update scholarship"""
        return service.update(id, scholarship_ns.payload)