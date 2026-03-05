from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.specialization_service import SpecializationService
from app.schemas.specialization_schema import SpecializationSchema
from app.utils import role_required

specialization_ns = Namespace("specializations", description="Specialization Management")
specialization_svc = SpecializationService(db.session)

specialization_response_schema = SpecializationSchema.get_schema(specialization_ns)
specialization_post_schema = SpecializationSchema.post_schema(specialization_ns)
specialization_filter_schema = SpecializationSchema.filter_schema(specialization_ns)
specialization_filter_response = SpecializationSchema.filter_response_schema(specialization_ns)

@specialization_ns.route("/")
class SpecializationList(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION", "USER")
    @specialization_ns.doc(security="Bearer Auth")
    @specialization_ns.marshal_list_with(specialization_response_schema)
    def get(self):
        """Get all specializations (Standard)"""
        return specialization_svc.get_all_specializations()
    
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION", "USER")
    @specialization_ns.doc(security="Bearer Auth")
    @specialization_ns.expect(specialization_filter_schema)
    @specialization_ns.response(200, "Success", specialization_filter_response)
    def post(self):
        """Search and Filter Specializations with Pagination"""
        return specialization_svc.get_specialization_list_filter(specialization_ns.payload)

@specialization_ns.route("/create")
class SpecializationCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @specialization_ns.doc(security="Bearer Auth")
    @specialization_ns.expect(specialization_post_schema)
    @specialization_ns.marshal_with(specialization_response_schema)
    def post(self):
        """Create a new specialization"""
        return specialization_svc.create_specialization(specialization_ns.payload)

@specialization_ns.route("/<int:id>")
class SpecializationDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION", "USER")
    @specialization_ns.doc(security="Bearer Auth")
    @specialization_ns.marshal_with(specialization_response_schema)
    def get(self, id):
        """Get specialization detail"""
        return specialization_svc.get_specialization_by_id(id)
    
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @specialization_ns.doc(security="Bearer Auth")
    @specialization_ns.expect(specialization_post_schema)
    @specialization_ns.marshal_with(specialization_response_schema)
    def put(self, id):
        """Update specialization detail"""
        return specialization_svc.update_specialization(id, specialization_ns.payload)
    
    @jwt_required()
    @role_required("ADMIN")
    @specialization_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """Delete a specialization"""
        return specialization_svc.delete_specialization(id)