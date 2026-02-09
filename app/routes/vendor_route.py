from flask_restx import Namespace, Resource, fields
from flask import request
from app.database import db
from app.services.vendor_service import VendorService
from app.schemas.vendor_schema import VendorSchema

vendor_ns = Namespace("vendors", description="Vendor endpoints")

vendor_schema = VendorSchema.get_schema(vendor_ns)

@vendor_ns.route("")
class VendorList(Resource):

    @vendor_ns.marshal_with(vendor_schema)
    def get(self):
        service = VendorService(db.session)
        return service.get_all()

    @vendor_ns.expect(vendor_ns.model("CreateVendor", {
        "name": fields.String(required=True),
        "initials": fields.String(required=True),
        "industry": fields.String(required=True),
        "company_type": fields.String,
        "service": fields.List(fields.String),
        "goods": fields.List(fields.String)
    }))
    def post(self):
        service = VendorService(db.session)
        return service.create(request.json)
