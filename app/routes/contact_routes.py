from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from app.database import db
from app.services.contact_service import ContactService
from app.schemas.contact_schema import ContactSchema
from app.utils import role_required

contact_ns = Namespace("contacts", description="Contact Management")
contact_svc = ContactService(db.session)
contact_response_schema = ContactSchema.get_schema(contact_ns)
contact_post_schema = ContactSchema.post_schema(contact_ns)
contact_filter_schema = ContactSchema.filter_schema(contact_ns)
contact_filter_response = ContactSchema.filter_response_schema(contact_ns)

@contact_ns.route("/")
class ContactList(Resource):
    
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @contact_ns.doc(security="Bearer Auth")
    @contact_ns.marshal_list_with(contact_response_schema)
    def get(self):
        """ Get all contacts (Standard) """
        return contact_svc.get_all_contacts()

    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @contact_ns.doc(security="Bearer Auth")
    @contact_ns.expect(contact_filter_schema)
    @contact_ns.response(200, "Success", contact_filter_response)
    def post(self):
        """ Search and Filter Contacts with Pagination """
        return contact_svc.get_contact_list_filter(contact_ns.payload)

@contact_ns.route("/create")
class ContactCreate(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @contact_ns.doc(security="Bearer Auth")
    @contact_ns.expect(contact_post_schema)
    @contact_ns.marshal_with(contact_response_schema)
    def post(self):
        """ Create a new contact """
        return contact_svc.create(contact_ns.payload)

@contact_ns.route("/<int:id>")
class ContactDetail(Resource):
    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE", "OPERATION", "USER")
    @contact_ns.doc(security="Bearer Auth")
    @contact_ns.marshal_with(contact_response_schema)
    def get(self, id):
        """ Get detail contact """
        return contact_svc.get_contact_by_id(id)

    @jwt_required()
    @role_required("ADMIN", "BIZDEV", "FINANCE")
    @contact_ns.doc(security="Bearer Auth")
    @contact_ns.expect(contact_post_schema)
    @contact_ns.marshal_with(contact_response_schema)
    def put(self, id):
        """ Update contact detail """
        return contact_svc.update(id, contact_ns.payload)

    @jwt_required()
    @role_required("ADMIN")
    @contact_ns.doc(security="Bearer Auth")
    def delete(self, id):
        """ Delete a contact """
        return contact_svc.delete(id)