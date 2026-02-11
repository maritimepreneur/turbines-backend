from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.vendor_service import VendorService
from app.schemas.vendor_schema import VendorSchema
from app.utils import role_required

vendor_ns = Namespace("vendors", description="Vendor Management")

# Inisialisasi service
vendor_svc = VendorService(db.session)

# Buat schema terpisah - PASTIKAN SEMUA METHOD ADA
vendor_response_schema = VendorSchema.get_schema(vendor_ns)
vendor_post_schema = VendorSchema.post_schema(vendor_ns)
vendor_filter_schema = VendorSchema.filter_schema(vendor_ns)  # Sekarang method ini ada
vendor_filter_response = VendorSchema.filter_response_schema(vendor_ns)  # Sekarang method ini ada
vendor_list_schema = VendorSchema.list_schema(vendor_ns)

@vendor_ns.route("/")
class VendorList(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @vendor_ns.doc(security="Bearer Auth")
    @vendor_ns.marshal_list_with(vendor_list_schema)
    def get(self):
        """Get all vendors (Standard) - Requires Auth"""
        return vendor_svc.get_all()
    
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @vendor_ns.doc(security="Bearer Auth")
    @vendor_ns.expect(vendor_filter_schema)
    @vendor_ns.response(200, "Success", vendor_filter_response)
    def post(self):
        """Search and Filter Vendors with Pagination - Requires Auth"""
        return vendor_svc.get_vendor_list_filter(vendor_ns.payload)

@vendor_ns.route("/create")
class VendorCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @vendor_ns.doc(security="Bearer Auth")
    @vendor_ns.expect(vendor_post_schema)
    @vendor_ns.marshal_with(vendor_response_schema, code=201)
    def post(self):
        """Create a new vendor - Requires Auth"""
        result = vendor_svc.create(vendor_ns.payload)
        
        if result.get("success") is False:
            vendor_ns.abort(400, result.get("message", "Bad Request"))
            
        return result, 201

@vendor_ns.route("/<int:id>")
class VendorDetail(Resource):
    # TANPA role required untuk GET (sesuai permintaan)
    @vendor_ns.marshal_with(vendor_response_schema)
    def get(self, id):
        """Get vendor by ID - Public Access"""
        result = vendor_svc.get_by_id(id)
        
        if result.get("success") is False:
            vendor_ns.abort(404, result.get("message", "Not Found"))
            
        return result
    
    # Tetap dengan role required untuk PUT dan DELETE
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @vendor_ns.doc(security="Bearer Auth")
    @vendor_ns.expect(vendor_post_schema)
    @vendor_ns.marshal_with(vendor_response_schema)
    def put(self, id):
        """Update vendor detail - Requires Auth"""
        result = vendor_svc.update(id, vendor_ns.payload)
        
        if result.get("success") is False:
            if "not found" in result.get("message", "").lower():
                vendor_ns.abort(404, result.get("message", "Not Found"))
            else:
                vendor_ns.abort(400, result.get("message", "Bad Request"))
                
        return result
    
    @jwt_required()
    @role_required("ADMIN")
    @vendor_ns.doc(security="Bearer Auth")
    @vendor_ns.response(200, "Vendor deleted successfully")
    @vendor_ns.response(404, "Vendor not found")
    def delete(self, id):
        """Delete a vendor - Requires Admin"""
        result = vendor_svc.delete(id)
        
        if result.get("success") is False:
            vendor_ns.abort(404, result.get("message", "Not Found"))
            
        return result