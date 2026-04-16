from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.models.quotations import Quotation
from app.models.contacts import Contact
from app.models.partners import Partner
from app.models.leads import Lead
from app.services.base_service import BaseService
from app.utils import response
from app.services.approval_service import ApprovalService

class QuotationService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Quotation)

    def get_all_quotations(self):
        """ Get all Quotation """
        quotations = self.db.query(Quotation).all()
        return response(200, "Success", quotations or [])
    
    def create_quotation(self, quotation_data):
        self.validate_fk(quotation_data)
        
        try:
            new_quotation = Quotation(**quotation_data)
            self.db.add(new_quotation)
            
            self.db.flush()
            self.db.refresh(new_quotation)

            approval_service = ApprovalService(self.db)
            approval_payload = {
                "entity_type": "Quotation",
                "quotation_id": new_quotation.id,
                "po_id": 0,
                "invoice_id": 0,
                "expense_id": 0,
                "creator_id": new_quotation.created_by, 
                "is_internal": True
            }
            approval_service.create(approval_payload)
            
            result_data = new_quotation.to_dict()
            
            self.db.commit()
            
            return {"code": 201, "message": "Success", "data": result_data}

        except Exception as e:

            self.db.rollback()
            print(f"ATOMIC TRANSACTION FAILED (Quotation): {str(e)}")
            raise e
    
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
            return response(404, f"Quotation ID {quotation_id} not found")
        return super().update(quotation_id, updated_data)
    
    def validate_fk(self, quotation_data):
        """ Existing validation logic """
        if quotation_data.get("contact_id") and not self.db.get(Contact, quotation_data["contact_id"]):
            return response(404, "Invalid contact_id")
        
        if quotation_data.get("partner_id") and not self.db.get(Partner, quotation_data["partner_id"]):
            return response(404, "Invalid partner_id")
        
        if quotation_data.get("lead_id") and not self.db.get(Lead, quotation_data["lead_id"]):
            return response(404, "Invalid lead_id")

    def get_quotation_list_filter(self, payload):
        """ New feature: Search, Filter, and Pagination for Quotations """
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')
            min_amount = payload.get('min_amount')
            max_amount = payload.get('max_amount')
            partner_ids = payload.get('partner_ids', [])

            query = self.db.query(Quotation)\
                .outerjoin(Partner, Quotation.partner_id == Partner.id)\
                .outerjoin(Lead, Quotation.lead_id == Lead.id)\
                .outerjoin(Contact, Quotation.contact_id == Contact.id)

            if search_query:
                query = query.filter(
                    or_(
                        Quotation.summary.ilike(f"%{search_query}%"),
                        Partner.name.ilike(f"%{search_query}%"),
                        Lead.name.ilike(f"%{search_query}%")
                    )
                )

            if min_amount is not None:
                query = query.filter(Quotation.total_amount >= min_amount)
            if max_amount is not None:
                query = query.filter(Quotation.total_amount <= max_amount)

            if partner_ids:
                query = query.filter(Quotation.partner_id.in_(partner_ids))

            sort_column = getattr(Quotation, sort_by) if hasattr(Quotation, sort_by) else Quotation.id
            query = query.order_by(desc(sort_column) if sort_order.upper() == 'DESC' else asc(sort_column))
            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            raw_data = query.offset(offset).limit(page_size).all()
            
            data_list = []
            for q in raw_data:
                item = q.to_dict()
                item["contact_name"] = q.contact.name if q.contact else None
                item["partner_name"] = q.partner.name if q.partner else None
                item["lead_name"] = q.lead.name if q.lead else None
                data_list.append(item)

            result = {
                "list": data_list,
                "pagination": {
                    "current_page": page_number,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "total_items": total_items
                }
            }
            return response(200, "Success", result)

        except Exception as e:
            return response(500, f"Error processing quotation filter: {str(e)}")