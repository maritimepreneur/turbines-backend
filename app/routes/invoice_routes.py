from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.invoice_service import InvoiceService
from app.schemas.invoice_schema import InvoiceSchema
from app.utils import role_required

invoice_ns = Namespace("invoices", description="Invoice Management")
invoice_svc = InvoiceService(db.session)
invoice_response_schema = InvoiceSchema.get_schema(invoice_ns)
invoice_post_schema = InvoiceSchema.post_schema(invoice_ns)
invoice_filter_schema = InvoiceSchema.filter_schema(invoice_ns)
invoice_filter_response = InvoiceSchema.filter_response_schema(invoice_ns)

@invoice_ns.route("/")
class InvoiceList(Resource):
    @jwt_required()
    @role_required("ADMIN", "FINANCE", "OPERATION")
    @invoice_ns.doc(security="Bearer Auth")
    @invoice_ns.response(200, "Success", invoice_response_schema)
    def get(self):
        """ Get all invoices """
        return invoice_svc.get_all_invoices()

    @jwt_required()
    @role_required("ADMIN", "FINANCE", "OPERATION")
    @invoice_ns.doc(security="Bearer Auth")
    @invoice_ns.expect(invoice_filter_schema)
    @invoice_ns.response(200, "Success", invoice_filter_response)
    def post(self):
        """ Search and Filter Invoices with Pagination """
        return invoice_svc.get_invoice_list_filter(invoice_ns.payload)

@invoice_ns.route("/create")
class InvoiceCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "FINANCE")
    @invoice_ns.doc(security="Bearer Auth")
    @invoice_ns.expect(invoice_post_schema)
    @invoice_ns.marshal_with(invoice_response_schema)
    def post(self):
        """ Create a new invoice """
        return invoice_svc.create_invoice(invoice_ns.payload)

@invoice_ns.route("/<int:id>")
class InvoiceDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "FINANCE", "OPERATION", "USER")
    @invoice_ns.doc(security="Bearer Auth")
    @invoice_ns.marshal_with(invoice_response_schema)
    def get(self, id):
        """ Get detail invoice """
        return invoice_svc.get_invoice_by_id(id)

    @jwt_required()
    @role_required("ADMIN", "FINANCE")
    @invoice_ns.doc(security="Bearer Auth")
    @invoice_ns.expect(invoice_post_schema)
    @invoice_ns.marshal_with(invoice_response_schema)
    def put(self, id):
        """ Update invoice detail """
        return invoice_svc.update_invoice(id, invoice_ns.payload)

    @jwt_required()
    @role_required("ADMIN")
    @invoice_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Delete an invoice """
        return invoice_svc.delete_invoice(id)