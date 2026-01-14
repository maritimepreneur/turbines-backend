from sqlalchemy.orm import Session
from app.models.partners import Partner
from app.services.base_service import BaseService
from app.utils import response

class PartnerService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Partner)

    def get_all_partners(self):
        """ Get all Partner """
        partners = self.db.query(Partner).all()
        return response(200, "Success", partners or [])
    
    def create(self, partner_data):
        """ Register a new Partner """
        return super().create(partner_data)
    
    def get_partner_by_id(self, partner_id):
        """ Get Partner details """
        partner = self._get_by_id(partner_id)
        if not partner:
            return response(404, "Partner not found", None)
        return super().get_by_id(partner_id)
    
    def update_partner_by_id(self, partner_id, updated_data):
        """ Update Partner """
        partner = self._get_by_id(partner_id)
        if not partner:
            return response(404, partner_id)
        return super().update(partner_id, updated_data)