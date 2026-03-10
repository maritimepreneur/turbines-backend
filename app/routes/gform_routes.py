from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.gform_service import GformService
from app.schemas.gform_schema import GformSchema
from app.utils import role_required

gform_ns = Namespace("gform", description="Google Form (Gform) Management")
gform_svc = GformService(db.session)

gform_response_schema = GformSchema.get_schema(gform_ns)
gform_post_schema = GformSchema.post_schema(gform_ns)
gform_filter_schema = GformSchema.filter_schema(gform_ns)
gform_filter_response = GformSchema.filter_response_schema(gform_ns)

@gform_ns.route("/")
class GformList(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR")
    @gform_ns.doc(security="Bearer Auth")
    @gform_ns.response(200, "Success", gform_response_schema)
    def get(self):
        """ Get all gforms (Simple List) """
        return gform_svc.get_all_gforms()

    @jwt_required()
    @role_required("ADMIN", "HR")
    @gform_ns.doc(security="Bearer Auth")
    @gform_ns.expect(gform_filter_schema)
    @gform_ns.response(200, "Success", gform_filter_response)
    def post(self):
        """ Search and Filter Gforms with Pagination """
        return gform_svc.get_gform_list_filter(gform_ns.payload)
    
@gform_ns.route("/create")
class GformCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR")
    @gform_ns.doc(security="Bearer Auth")
    @gform_ns.expect(gform_post_schema)
    @gform_ns.marshal_with(gform_response_schema)
    def post(self):
        """ Create a new gform entry """
        return gform_svc.create_gform(gform_ns.payload)
    
@gform_ns.route("/<int:id>")
class GformDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR")
    @gform_ns.doc(security="Bearer Auth")
    @gform_ns.marshal_with(gform_response_schema)
    def get(self, id):
        """ Get detail gform """
        return gform_svc.get_gform_by_id(id)
    
    @jwt_required()
    @role_required("ADMIN", "HR")
    @gform_ns.doc(security="Bearer Auth")
    @gform_ns.expect(gform_post_schema)
    @gform_ns.marshal_with(gform_response_schema)
    def put(self, id):
        """ Update gform detail """
        return gform_svc.update_gform_by_id(id, gform_ns.payload)
    
    @jwt_required()
    @role_required("ADMIN", "HR")
    @gform_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Delete a gform entry """
        return gform_svc.delete(id)