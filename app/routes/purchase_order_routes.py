from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.purchase_order_service import PurchaseOrderService
from app.schemas.purchase_order_schema import PurchaseOrderSchema
from app.utils import role_required

purchase_order_ns = Namespace("purchase-orders", description="Purchase Order Management")

service = PurchaseOrderService(db.session)

purchase_response_schema = PurchaseOrderSchema.get_schema(purchase_order_ns)
purchase_post_schema = PurchaseOrderSchema.post_schema(purchase_order_ns)

@purchase_order_ns.route("/")
class PurchaseOrderList(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @purchase_order_ns.doc(security="Bearer Auth")
    @purchase_order_ns.marshal_list_with(purchase_response_schema)
    def get(self):
        """ Get all purchase orders """
        return service.get_all()

@purchase_order_ns.route("/create")
class PurchaseOrderCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @purchase_order_ns.doc(security="Bearer Auth")
    @purchase_order_ns.expect(purchase_post_schema)
    @purchase_order_ns.marshal_with(purchase_response_schema)
    def post(self):
        """ Create a new purchase order """
        return service.create_purchase(purchase_order_ns.payload)

@purchase_order_ns.route("/<int:id>")
class PurchaseOrderDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @purchase_order_ns.doc(security="Bearer Auth")
    @purchase_order_ns.marshal_with(purchase_response_schema)
    def get(self, id):
        """ Get detail purchase order """
        return service.get_by_id(id)

    @jwt_required()
    @role_required("ADMIN")
    @purchase_order_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Delete a purchase order """
        return service.delete(id)

@purchase_order_ns.route("/update/<int:id>")
class PurchaseOrderUpdate(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @purchase_order_ns.doc(security="Bearer Auth")
    @purchase_order_ns.expect(purchase_post_schema)
    @purchase_order_ns.marshal_with(purchase_response_schema)
    def put(self, id):
        """ Update purchase order detail """
        return service.update_purchase(id, purchase_order_ns.payload)