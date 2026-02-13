from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from flask import request
from app.database import db
from app.services.payment_service import PaymentService
from app.schemas.payment_schema import PaymentSchema
from app.utils import role_required

payment_ns = Namespace("payments", description="Payment Management")
service = PaymentService(db.session)

# Load Schemas
payment_detail_schema = PaymentSchema.get_schema(payment_ns)
payment_post_schema = PaymentSchema.post_schema(payment_ns)
payment_filter_schema = PaymentSchema.filter_response_schema(payment_ns)

@payment_ns.route("/")
class PaymentList(Resource):
    @jwt_required()
    @role_required("ADMIN", "FINANCE")
    @payment_ns.doc(security="Bearer Auth")
    @payment_ns.marshal_with(payment_filter_schema)
    def get(self):
        """ Get all payments with pagination """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        return service.get_all(page, per_page)

@payment_ns.route("/create")
class PaymentCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "FINANCE")
    @payment_ns.doc(security="Bearer Auth")
    @payment_ns.expect(payment_post_schema)
    @payment_ns.marshal_with(payment_detail_schema)
    def post(self):
        """ Create a new payment """
        return service.create_payment(payment_ns.payload)

@payment_ns.route("/<int:id>")
class PaymentDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "FINANCE")
    @payment_ns.doc(security="Bearer Auth")
    @payment_ns.marshal_with(payment_detail_schema)
    def get(self, id):
        """ Get detail payment """
        return service.get_by_id(id)

    @jwt_required()
    @role_required("ADMIN")
    @payment_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Delete a payment """
        return service.delete(id)

@payment_ns.route("/update/<int:id>")
class PaymentUpdate(Resource):
    @jwt_required()
    @role_required("ADMIN", "FINANCE")
    @payment_ns.doc(security="Bearer Auth")
    @payment_ns.expect(payment_post_schema)
    @payment_ns.marshal_with(payment_detail_schema)
    def put(self, id):
        """ Update payment detail """
        return service.update_payment(id, payment_ns.payload)