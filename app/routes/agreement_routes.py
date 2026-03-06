from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.agreement_service import AgreementService
from app.schemas.agreement_schema import AgreementSchema
from app.utils import role_required

agreement_ns = Namespace("agreements", description="Agreements Management")
agreement_svc = AgreementService(db.session)

# Schema definitions for documentation
agreement_response_schema = AgreementSchema.get_schema(agreement_ns)
agreement_post_schema = AgreementSchema.post_schema(agreement_ns)

@agreement_ns.route("/")
class AgreementList(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @agreement_ns.doc(security="Bearer Auth")
    @agreement_ns.response(200, "Success") # Menggunakan list filter jika ingin pagination
    def get(self):
        """Get All Agreements (Simple List)"""
        # Kita bisa memanggil filter dengan payload kosong untuk mendapatkan semua
        return agreement_svc.get_agreement_list_filter({})

    @jwt_required()
    @role_required("ADMIN", "HR")
    @agreement_ns.doc(security="Bearer Auth")
    @agreement_ns.expect(agreement_post_schema)
    @agreement_ns.marshal_with(agreement_response_schema)
    def post(self):
        """Create a new Agreement (Include Partners)"""
        return agreement_svc.create_agreement(agreement_ns.payload or {})

@agreement_ns.route("/filter")
class AgreementFilter(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @agreement_ns.doc(security="Bearer Auth")
    @agreement_ns.expect(agreement_ns.model("AgreementFilter", {
        "page_size": fields.Integer(default=10, description="Jumlah data per halaman"),
        "page_number": fields.Integer(default=1, description="Nomor halaman"),
        "search": fields.String(default="", description="Kata kunci pencarian"),
        "sort_order": fields.String(default="DESC", description="Urutan (ASC/DESC)")
    }))
    def post(self):
        """Search and Filter Agreements"""
        return agreement_svc.get_agreement_list_filter(agreement_ns.payload)

@agreement_ns.route("/<int:id>")
class AgreementResource(Resource):
    @jwt_required()
    @role_required("ADMIN", "HR", "OPERATION")
    @agreement_ns.doc(security="Bearer Auth")
    @agreement_ns.marshal_with(agreement_response_schema)
    def get(self, id):
        """Get specific agreement detail"""
        return agreement_svc.get_agreement_by_id(id)

    @jwt_required()
    @role_required("ADMIN", "HR")
    @agreement_ns.doc(security="Bearer Auth")
    @agreement_ns.expect(agreement_post_schema)
    @agreement_ns.marshal_with(agreement_response_schema)
    def put(self, id):
        """Update an existing agreement"""
        return agreement_svc.update_agreement(id, agreement_ns.payload or {})

    @jwt_required()
    @role_required("ADMIN", "HR")
    @agreement_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """Delete an agreement record"""
        return agreement_svc.delete_agreement(id)