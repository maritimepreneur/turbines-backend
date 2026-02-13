from flask_restx import Namespace, Resource
from flask import request
from app.services.items_services import ItemsService
from app.schemas.items_schema import ItemsSchema


items_ns = Namespace("items", description="Items operations")

create_model = ItemsSchema.create_schema(items_ns)
response_model = ItemsSchema.response_schema(items_ns)


@items_ns.route("/")
class ItemsList(Resource):

    @items_ns.marshal_with(response_model)
    def get(self):
        data = ItemsService.get_all()
        return {
            "success": True,
            "message": "Items retrieved successfully",
            "data": data
        }


@items_ns.route("/create")
class ItemsCreate(Resource):

    @items_ns.expect(create_model)
    @items_ns.marshal_with(response_model)
    def post(self):
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
