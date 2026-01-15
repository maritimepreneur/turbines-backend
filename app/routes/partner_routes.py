from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.partner_service import PartnerService
from app.schemas.partner_schema import PartnerSchema
from app.utils import role_required

partner_ns = Namespace("partners", description="Partner Management")
partner_svc = PartnerService(db.session)
partner_response_schema = PartnerSchema.get_schema(partner_ns)
partner_post_schema = PartnerSchema.post_schema(partner_ns)

@partner_ns.route("/")
class PartnerList(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @partner_ns.doc(security="Bearer Auth")
    @partner_ns.marshal_list_with(partner_response_schema)
    def get(self):
        """ Get all partners """
        return partner_svc.get_all_partners()
    
@partner_ns.route("/create")
class PartnerCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @partner_ns.doc(security="Bearer Auth")
    @partner_ns.expect(partner_post_schema)
    @partner_ns.marshal_with(partner_response_schema)
    def post(self):
        """ Create a new partner """
        return partner_svc.create(partner_ns.payload)
    
@partner_ns.route("/<int:id>")
class PartnerDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @partner_ns.doc(security="Bearer Auth")
    @partner_ns.marshal_with(partner_response_schema)
    def get(self, id):
        """ Get detail partner """
        return partner_svc.get_partner_by_id(id)
    
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @partner_ns.doc(security="Bearer Auth")
    @partner_ns.expect(partner_post_schema)
    @partner_ns.marshal_with(partner_response_schema)
    def put(self, id):
        """ Update partner detail """
        return partner_svc.update(id, partner_ns.payload)
    
    @jwt_required()
    @role_required("ADMIN")
    @partner_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Delete a partner """
        return partner_svc.delete(id)