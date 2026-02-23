from flask_restx import Namespace, Resource
from flask import request
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

    @items_ns.marshal_with(response_model)
    def get(self):
        """ Get all items """
        data = ItemsService.get_all()
        return {
            "success": True,
            "message": "Items retrieved successfully",
            "data": data
        }

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

    @items_ns.expect(create_model)
    @items_ns.marshal_with(response_model)
    def post(self):
        """ Create a new item """
        data = request.json
        item = ItemsService.create(data)

        return {
            "success": True,
            "message": "Item created successfully",
            "data": item
        }

@items_ns.route("/<int:item_id>")
class ItemsDetail(Resource):

    @items_ns.marshal_with(response_model)
    def get(self, item_id):
        """ Get item detail by ID """
        item = ItemsService.get_by_id(item_id)
        if not item:
            return {
                "success": False,
                "message": "Item not found",
                "data": None
            }, 404

        return {
            "success": True,
            "message": "Item retrieved successfully",
            "data": item
        }

    @items_ns.expect(create_model)
    @items_ns.marshal_with(response_model)
    def put(self, item_id):
        """ Update item detail """  # <--- Keterangan untuk PUT /api/items/{item_id}
        data = request.json
        item = ItemsService.update(item_id, data)

        if not item:
            return {
                "success": False,
                "message": "Item not found",
                "data": None
            }, 404

        return {
            "success": True,
            "message": "Item updated successfully",
            "data": item
        }

    def delete(self, item_id):
        """ Delete an item """ 
        success = ItemsService.delete(item_id)

        if not success:
            return {
                "success": False,
                "message": "Item not found"
            }, 404

        return {
            "success": True,
            "message": "Item deleted successfully"
        }