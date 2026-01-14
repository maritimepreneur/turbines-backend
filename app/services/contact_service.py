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
        emails = contact_data.get("emails")
        phones = contact_data.get("phone_numbers")

        if not isinstance(emails, list) or not isinstance(phones, list):
            return response(400, "emails and phone_numbers must be list")

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
        
        if "emails" in updated_data:
            contact.emails = list(set(contact.emails + updated_data["emails"]))

        if "phone_numbers" in updated_data:
            contact.phone_numbers = list(set(contact.phone_numbers + updated_data["phone_numbers"]))

        self.db.commit()
        self.db.refresh(contact)
        return response(200, "Action Success", contact)