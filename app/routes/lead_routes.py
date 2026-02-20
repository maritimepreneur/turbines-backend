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
lead_filter_schema = LeadSchema.filter_schema(lead_ns)
lead_filter_response = LeadSchema.filter_response_schema(lead_ns)
lead_dropdown_schema = LeadSchema.dropdown_list_schema(lead_ns)
lead_stage_update_schema = LeadSchema.stage_update_schema(lead_ns)
lead_pipeline_schema = LeadSchema.pipeline_summary_schema(lead_ns)

@lead_ns.route("/contact-list")
class LeadContactList(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @lead_ns.doc(security="Bearer Auth")
    @lead_ns.marshal_with(lead_dropdown_schema)
    def get(self):
        """ Get list of contacts (ID & Name only) for dropdown """
        return lead_svc.get_contact_list_dropdown()

@lead_ns.route("/partner-list")
class LeadPartnerList(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @lead_ns.doc(security="Bearer Auth")
    @lead_ns.marshal_with(lead_dropdown_schema)
    def get(self):
        """ Get list of partners (ID & Name only) for dropdown """
        return lead_svc.get_partner_list_dropdown()

@lead_ns.route("/summary")
class LeadPipelineSummary(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @lead_ns.doc(security="Bearer Auth")
    @lead_ns.marshal_with(lead_pipeline_schema)
    def get(self):
        """Get lead counts per stage for pipeline view"""
        return lead_svc.get_pipeline_summary()

@lead_ns.route("/<int:id>/stage")
class LeadStageUpdate(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @lead_ns.doc(security="Bearer Auth")
    @lead_ns.expect(lead_stage_update_schema)
    @lead_ns.marshal_with(lead_response_schema)
    def patch(self, id):
        """Update lead stage only"""
        return lead_svc.update_lead_stage(id, lead_ns.payload['stage'])

@lead_ns.route("/")
class LeadList(Resource):    
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @lead_ns.doc(security="Bearer Auth")
    @lead_ns.expect(lead_filter_schema)
    @lead_ns.response(200, "Success", lead_filter_response)
    def post(self):
        """ Search and Filter Leads with Pagination """
        return lead_svc.get_lead_list_filter(lead_ns.payload)

@lead_ns.route("/create")
class LeadCreate(Resource):
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
