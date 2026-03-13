from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.utils import role_required
from app.services.item_services import ItemsService
from app.schemas.item_schema import ItemsSchema

items_ns = Namespace("items", description="Item Management")
item_svc = ItemsService(db.session)
create_model = ItemsSchema.create_schema(items_ns)
response_model = ItemsSchema.response_schema(items_ns)
filter_model = ItemsSchema.filter_schema(items_ns)
filter_response = ItemsSchema.filter_response_schema(items_ns)


@items_ns.route("/")
class ItemsList(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @items_ns.doc(security="Bearer Auth")
    @items_ns.marshal_with(response_model)
    def get(self):
        """ Get all items """
        return item_svc.get_all_items()

    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @items_ns.doc(security="Bearer Auth")
    @items_ns.expect(filter_model)
    @items_ns.response(200, "Success", filter_response)
    def post(self):
        """ Search and Filter Items with Pagination """
        return item_svc.get_item_list_filter(items_ns.payload)


@items_ns.route("/create")
class ItemsCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION")
    @items_ns.doc(security="Bearer Auth")
    @items_ns.expect(create_model)
    @items_ns.marshal_with(response_model)
    def post(self):
        """ Create a new item """
        return item_svc.create(items_ns.payload)

@items_ns.route("/<int:item_id>")
class ItemsDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @items_ns.doc(security="Bearer Auth")
    @items_ns.marshal_with(response_model)
    def get(self, item_id):
        """ Get item detail by ID """
        return item_svc.get_item_by_id(item_id)

    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION")
    @items_ns.doc(security="Bearer Auth")
    @items_ns.expect(create_model)
    @items_ns.marshal_with(response_model)
    def put(self, item_id):
        """ Update item detail """
        return item_svc.update_item_by_id(item_id, items_ns.payload)

    @jwt_required()
    @role_required("ADMIN")
    @items_ns.doc(security="Bearer Auth")
    def delete(self, item_id):
        """ Delete an item """ 
        return item_svc.delete(item_id)
