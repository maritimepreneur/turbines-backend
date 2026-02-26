from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.document_service import DocumentService
from app.schemas.document_schema import DocumentSchema
from app.utils import role_required

document_ns = Namespace("documents", description="Document Management")
document_svc = DocumentService(db.session)
document_response_schema = DocumentSchema.get_schema(document_ns)
document_post_schema = DocumentSchema.post_schema(document_ns)
document_list_response = DocumentSchema.list_response_schema(document_ns)
document_filter_schema = DocumentSchema.filter_schema(document_ns)
document_filter_response = DocumentSchema.filter_response_schema(document_ns)

@document_ns.route("/")
class DocumentList(Resource):
    
    @jwt_required()
    @role_required("ADMIN", "HR", "BISDEV")
    @document_ns.doc(security="Bearer Auth")
    @document_ns.response(200, "Success Retrieve All Data", document_list_response)
    def get(self):
        """ Ambil semua data dokumen """
        return document_svc.get_all_documents()

    @jwt_required()
    @role_required("ADMIN", "HR", "BISDEV")
    @document_ns.doc(security="Bearer Auth")
    @document_ns.expect(document_filter_schema)
    @document_ns.response(200, "Success Filter Data", document_filter_response)
    def post(self):
        """ Cari dan Filter dokumen (Search, Sort, Pagination) """
        return document_svc.get_document_list_filter(document_ns.payload)

@document_ns.route("/create")
class DocumentCreate(Resource):
    
    @jwt_required()
    @role_required("ADMIN", "BISDEV")
    @document_ns.doc(security="Bearer Auth")
    @document_ns.expect(document_post_schema)
    @document_ns.marshal_with(document_response_schema)
    def post(self):
        """ Membuat data dokumen baru """
        return document_svc.create(document_ns.payload)

@document_ns.route("/<int:id>")
class DocumentDetail(Resource):
    
    @jwt_required()
    @role_required("ADMIN", "HR", "BISDEV")
    @document_ns.doc(security="Bearer Auth")
    @document_ns.marshal_with(document_response_schema)
    def get(self, id):
        """ Ambil detail dokumen berdasarkan ID """
        return document_svc.get_document_by_id(id)

    @jwt_required()
    @role_required("ADMIN", "BISDEV")
    @document_ns.doc(security="Bearer Auth")
    @document_ns.expect(document_post_schema)
    @document_ns.marshal_with(document_response_schema)
    def put(self, id):
        """ Update data dokumen """
        return document_svc.update(id, document_ns.payload)

    @jwt_required()
    @role_required("ADMIN")
    @document_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Menghapus data dokumen """
        return document_svc.delete(id)