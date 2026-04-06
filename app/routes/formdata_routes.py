from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.formdata_service import FormDataService
from app.schemas.formdata_schema import FormDataSchema
from app.utils import role_required

formdata_ns = Namespace("formdata", description="Form Data Management")

formdata_svc = FormDataService(db.session)

formdata_response_schema = FormDataSchema.get_schema(formdata_ns)
formdata_post_schema = FormDataSchema.post_schema(formdata_ns)
formdata_filter_schema = FormDataSchema.filter_schema(formdata_ns)
formdata_filter_response = FormDataSchema.filter_response_schema(formdata_ns)
formdata_update_schema = FormDataSchema.post_schema(formdata_ns) 

@formdata_ns.route("/")
class FormDataList(Resource):

    @jwt_required()
    @role_required("ADMIN", "FINANCE", "BIZDEV")
    @formdata_ns.doc(security="Bearer Auth")
    @formdata_ns.response(200, "Success", formdata_response_schema)
    def get(self):
        """Get all formdata (simple list)"""
        return formdata_svc.get_all_formdata()

    @jwt_required()
    @role_required("ADMIN", "FINANCE", "BIZDEV")
    @formdata_ns.doc(security="Bearer Auth")
    @formdata_ns.expect(formdata_filter_schema)
    @formdata_ns.response(200, "Success", formdata_filter_response)
    def post(self):
        """Search and filter formdata with pagination"""
        return formdata_svc.get_formdata_list_filter(formdata_ns.payload)


@formdata_ns.route("/create")
class FormDataCreate(Resource):

    @jwt_required()
    @role_required("ADMIN", "FINANCE", "BIZDEV")
    @formdata_ns.doc(security="Bearer Auth")
    @formdata_ns.expect(formdata_post_schema)
    @formdata_ns.marshal_with(formdata_response_schema)
    def post(self):
        """Create new formdata"""
        return formdata_svc.create_formdata(formdata_ns.payload)


@formdata_ns.route("/<int:id>")
class FormDataDetail(Resource):

    @jwt_required()
    @role_required("ADMIN", "FINANCE", "BIZDEV")
    @formdata_ns.doc(security="Bearer Auth")
    @formdata_ns.marshal_with(formdata_response_schema)
    def get(self, id):
        """Get formdata detail"""
        return formdata_svc.get_formdata_by_id(id)

    @jwt_required()
    @role_required("ADMIN", "FINANCE")
    @formdata_ns.doc(security="Bearer Auth")
    @formdata_ns.expect(formdata_post_schema) 
    @formdata_ns.marshal_with(formdata_response_schema)
    def put(self, id):
        """Update selection status or interview"""
        return formdata_svc.update_selection(id, formdata_ns.payload)

    @jwt_required()
    @role_required("ADMIN")
    @formdata_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """Delete formdata"""
        return formdata_svc.delete_formdata(id)