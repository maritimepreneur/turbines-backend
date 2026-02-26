from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.quotation_service import QuotationService
from app.schemas.quotation_schema import QuotationSchema
from app.utils import role_required

quotation_ns = Namespace("quotations", description="Quotation Management")
quotation_svc = QuotationService(db.session)
quotation_response_schema = QuotationSchema.get_schema(quotation_ns)
quotation_post_schema = QuotationSchema.post_schema(quotation_ns)
quotation_filter_schema = QuotationSchema.filter_schema(quotation_ns)
quotation_filter_response = QuotationSchema.filter_response_schema(quotation_ns)

@quotation_ns.route("/")
class QuotationList(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION")
    @quotation_ns.doc(security="Bearer Auth")
    @quotation_ns.expect(quotation_filter_schema)
    @quotation_ns.response(200, "Success", quotation_filter_response)
    def post(self):
        """ Search and Filter Quotations with Pagination """
        return quotation_svc.get_quotation_list_filter(quotation_ns.payload)

    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION")
    @quotation_ns.doc(security="Bearer Auth")
    @quotation_ns.marshal_list_with(quotation_response_schema)
    def get(self):
        """ Get all quotations (Simple List) """
        return quotation_svc.get_all_quotations()
    
@quotation_ns.route("/create")
class QuotationCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV")
    @quotation_ns.doc(security="Bearer Auth")
    @quotation_ns.expect(quotation_post_schema)
    @quotation_ns.marshal_with(quotation_response_schema)
    def post(self):
        """ Create a new quotation """
        return quotation_svc.create_quotation(quotation_ns.payload)
    
@quotation_ns.route("/<int:id>")
class QuotationDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @quotation_ns.doc(security="Bearer Auth")
    @quotation_ns.marshal_with(quotation_response_schema)
    def get(self, id):
        """ Get detail quotation """
        return quotation_svc.get_quotation_by_id(id)
    
    @jwt_required()
    @role_required("ADMIN", "BIZDEV")
    @quotation_ns.doc(security="Bearer Auth")
    @quotation_ns.expect(quotation_post_schema)
    @quotation_ns.marshal_with(quotation_response_schema)
    def put(self, id):
        """ Update quotation detail """
        return quotation_svc.update_quotation_by_id(id, quotation_ns.payload)
    
    @jwt_required()
    @role_required("ADMIN")
    @quotation_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Delete a quotation """
        return quotation_svc.delete(id)