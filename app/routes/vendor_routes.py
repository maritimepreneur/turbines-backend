from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.vendor_service import VendorService
from app.schemas.vendor_schema import VendorSchema
from app.utils import role_required

vendor_ns = Namespace("vendors", description="Vendor Management")
vendor_svc = VendorService(db.session)
vendor_response_schema = VendorSchema.get_schema(vendor_ns)
vendor_post_schema = VendorSchema.post_schema(vendor_ns)
vendor_filter_schema = VendorSchema.filter_schema(vendor_ns)
vendor_filter_response = VendorSchema.filter_response_schema(vendor_ns)

@vendor_ns.route("/")
class VendorList(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @vendor_ns.doc(security="Bearer Auth")
    @vendor_ns.expect(vendor_filter_schema)
    @vendor_ns.response(200, "Success", vendor_filter_response)
    def post(self):
        """Search and Filter Vendors with Pagination"""
        return vendor_svc.get_vendor_list_filter(vendor_ns.payload)

@vendor_ns.route("/create")
class VendorCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @vendor_ns.doc(security="Bearer Auth")
    @vendor_ns.expect(vendor_post_schema)
    @vendor_ns.marshal_with(vendor_response_schema, code=201)
    def post(self):
        """Create a new vendor"""
        return vendor_svc.create_vendor(vendor_ns.payload)

@vendor_ns.route("/<int:id>")
class VendorDetail(Resource):
    @jwt_required()
    @vendor_ns.doc(security="Bearer Auth")
    @vendor_ns.marshal_with(vendor_response_schema)
    def get(self, id):
        """Get vendor detail by ID"""
        return vendor_svc.get_by_id(id)

    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @vendor_ns.doc(security="Bearer Auth")
    @vendor_ns.expect(vendor_post_schema)
    @vendor_ns.marshal_with(vendor_response_schema)
    def put(self, id):
        """Update vendor detail"""
        return vendor_svc.update(id, vendor_ns.payload)

    @jwt_required()
    @role_required("ADMIN")
    @vendor_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """Delete a vendor"""
        return vendor_svc.delete(id)