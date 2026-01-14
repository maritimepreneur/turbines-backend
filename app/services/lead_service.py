from sqlalchemy.orm import Session
from app.services.base_service import BaseService
from app.models.leads import Lead
from app.utils import response

class LeadService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Lead)
    
    def get_all_leads(self):
        return self.get_all()
    
    def get_lead_by_id(self, lead_id: int):
        return self.get_by_id(lead_id)
    
    def create_lead(self, data):
        return self.create(data)
    
    def update_lead(self, lead_id: int, data):
        return self.update(lead_id, data)
    
    def delete_lead(self, lead_id: int):
        return self.delete(lead_id)