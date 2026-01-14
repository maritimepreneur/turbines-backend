from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.lead_service import LeadService
from app.schemas.lead_schema import LeadSchema
from app.utils import role_required

lead_ns = Namespace("leads", description="Lead Management")
lead_svc = LeadService(db.session)
lead_response_schema = LeadSchema.get_schema(lead_ns)
lead_post_schema = LeadSchema.post_schema(lead_ns)

@lead_ns.route("/")
class LeadList(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @lead_ns.doc(security="Bearer Auth")
    @lead_ns.marshal_list_with(lead_response_schema)
    def get(self):
        """ Get all leads """
        return lead_svc.get_all_leads()
    
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @lead_ns.doc(security="Bearer Auth")
    @lead_ns.expect(lead_post_schema)
    @lead_ns.marshal_with(lead_response_schema)
    def post(self):
        """ Create a new lead """
        return lead_svc.create_lead(lead_ns.payload)
    
@lead_ns.route("/<int:id>")
class LeadDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @lead_ns.doc(security="Bearer Auth")
    @lead_ns.marshal_with(lead_response_schema)
    def get(self, id):
        """ Get lead detail """
        return lead_svc.get_lead_by_id(id)
    
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @lead_ns.doc(security="Bearer Auth")
    @lead_ns.expect(lead_post_schema)
    @lead_ns.marshal_with(lead_response_schema)
    def put(self, id):
        """ Update lead detail """
        return lead_svc.update_lead(id, lead_ns.payload)
    
    @jwt_required()
    @role_required("ADMIN")
    @lead_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Delete a lead """
        return lead_svc.delete_lead(id)