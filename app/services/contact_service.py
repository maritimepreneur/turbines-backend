from sqlalchemy.orm import Session
from app.models.contacts import Contact
from app.services.base_service import BaseService
from app.utils import response

class ContactService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Contact)
    
    def get_all_contacts(self):
        """ Get All Contact """
        contacts = self.db.query(Contact).all()
        return response(200, "Success", contacts)
    
    def create(self, contact_data):
        """" Register a new contact """
        return super().create(contact_data)
    
    def get_contact_by_id(self, contact_id):
        """ Get Contact details """
        contact = self._get_by_id(contact_id)
        if not contact:
            return response(404, "Contact not found")
        return super().get_by_id(contact_id)
    
    def update_contact_by_id(self, contact_id, updated_data):
        """ Update Contact """
        contact = self._get_by_id(contact_id)
        if not contact:
            return response(404, contact_id)
        return super().update(contact_id, updated_data)