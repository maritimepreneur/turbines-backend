from sqlalchemy.orm import Session
from app.models.quotations import Quotation
from app.models.contacts import Contact
from app.models.partners import Partner
from app.models.leads import Lead
from app.services.base_service import BaseService
from app.utils import response

class QuotationService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Quotation)

    def get_all_quotations(self):
        """ Get all Quotation """
        quotations = self.db.query(Quotation).all()
        return response(200, "Success", quotations or [])
    
    def create_quotation(self, quotation_data):
        """ Create a new quotation """
        self.validate_fk(quotation_data)
        return super().create(quotation_data)
    
    def get_quotation_by_id(self, quotation_id):
        """ Get Quotation details """
        quotation = self._get_by_id(quotation_id)
        if not quotation:
            return response(404, "Quotation not found", None)
        return super().get_by_id(quotation_id)
    
    def update_quotation_by_id(self, quotation_id, updated_data):
        """ Update Quotation """
        quotation = self._get_by_id(quotation_id)
        self.validate_fk(updated_data)
        if not quotation:
            return response(404, quotation_id)
        return super().update(quotation_id, updated_data)
    
    def validate_fk(self, quotation_data):
        if quotation_data("contact_id") and not self.db.get(Contact, quotation_data["contact_id"]):
            return response(404, "Invalid contact_id")
        
        if quotation_data("partner_id") and not self.db.get(Partner,quotation_data["partner_id"]):
            return response(404, "Invalid partner_id")
        
        if quotation_data("lead_id") and not self.db.get(Lead, quotation_data["lead_id"]):
            return response(404, "Invalid lead_id")