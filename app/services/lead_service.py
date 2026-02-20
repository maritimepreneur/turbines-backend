from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc, func
from app.services.base_service import BaseService
from app.models.leads import Lead
from app.models.contacts import Contact
from app.models.partners import Partner
from app.models.leads import Stages
from app.utils import response

class LeadService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Lead)
    
    def get_all_leads(self):
        data = [x.to_dict() for x in self.db.query(Lead).all()]
        return response(200, "Success", data)

    def get_lead_by_id(self, lead_id: int):
        return self.get_by_id(lead_id)
    
    def create_lead(self, data):
        return self.create(data)
    
    def update_lead(self, lead_id: int, data):
        return self.update(lead_id, data)
    
    def delete_lead(self, lead_id: int):
        return self.delete(lead_id)

    def get_lead_list_filter(self, payload):
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')

            period_start = payload.get('period_start')
            period_end = payload.get('period_end')
            contacts_filter = payload.get('contacts', [])
            partners_filter = payload.get('partners', [])
            stages_filter = payload.get('stages', []) 

            query = self.db.query(Lead)\
                .outerjoin(Contact, Lead.contact_id == Contact.id)\
                .outerjoin(Partner, Lead.partner_id == Partner.id)

            if search_query:
                query = query.filter(
                    or_(
                        Lead.name.ilike(f"%{search_query}%"),
                        Contact.company.ilike(f"%{search_query}%")
                    )
                )

            if period_start and period_end:
                query = query.filter(Lead.period.between(period_start, period_end))

            if contacts_filter:
                conditions = [Contact.name.ilike(f"%{c}%") for c in contacts_filter if c]
                if conditions:
                    query = query.filter(or_(*conditions))

            if partners_filter:
                conditions = [Partner.name.ilike(f"%{p}%") for p in partners_filter if p]
                if conditions:
                    query = query.filter(or_(*conditions))
            if stages_filter:
                conditions = [Stages[s.upper()] for s in stages_filter if s.upper() in [stage.name for stage in Stages]]
                if conditions:
                    query = query.filter(Lead.current_stages.in_(conditions))

            if hasattr(Lead, sort_by):
                sort_column = getattr(Lead, sort_by)
            elif sort_by == 'company':
                sort_column = Contact.company
            elif sort_by == 'contact_name':
                sort_column = Contact.name
            elif sort_by == 'partner_name':
                sort_column = Partner.name
            else:
                sort_column = Lead.id 

            if sort_order.upper() == 'DESC':
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            
            raw_data = query.offset(offset).limit(page_size).all()
            
            data = [lead.to_dict() for lead in raw_data]

            result = {
                "list": data,
                "pagination": {
                    "current_page": page_number,
                    "page_size": page_size,
                    "total_pages": total_pages,
                    "total_items": total_items
                }
            }
            
            return response(200, "Success", result)

        except Exception as e:
            print(f"Error filtering leads: {e}")
            return response(500, f"Error processing lead filter: {str(e)}")

    def get_contact_list_dropdown(self):
        """ Get lightweight contact list for dropdowns """
        try:
            contacts = self.db.query(Contact.id, Contact.name).all()
            result = [{"id": c.id, "name": c.name} for c in contacts]
            return response(200, "Success", result)
        except Exception as e:
            return response(500, f"Error fetching contact list: {str(e)}")

    def get_partner_list_dropdown(self):
        """ Get lightweight partner list for dropdowns """
        try:
            partners = self.db.query(Partner.id, Partner.name).all()
            result = [{"id": p.id, "name": p.name} for p in partners]
            return response(200, "Success", result)
        except Exception as e:
            return response(500, f"Error fetching partner list: {str(e)}")

    def get_pipeline_summary(self):
        """Get count of leads per stage for pipeline view"""
        try:
            results = self.db.query(
                Lead.current_stages,
                func.count(Lead.id).label('count')
            ).group_by(Lead.current_stages).all()
            
            summary = {stage.name: 0 for stage in Stages}
            
            for stage, count in results:
                summary[stage.name] = count
            
            pipeline = [
                {
                    "stage": stage.name,
                    "label": stage.value,
                    "count": summary[stage.name]
                }
                for stage in Stages
            ]
            
            return response(200, "Success", pipeline)
        except Exception as e:
            return response(500, f"Error fetching pipeline summary: {str(e)}")

    def update_lead_stage(self, lead_id: int, new_stage: str):
        """Update lead stage"""
        try:
            from app.models.leads import Stages
            
            if new_stage.upper() not in [s.name for s in Stages]:
                return response(400, f"Invalid stage. Valid stages: {[s.name for s in Stages]}")
            
            lead = self._get_by_id(lead_id)
            if not lead:
                return response(404, "Lead not found")
            
            lead.current_stages = Stages[new_stage.upper()]
            self.db.commit()
            self.db.refresh(lead)
            
            return response(200, "Stage updated successfully", lead)
        except Exception as e:
            self.db.rollback()
            return response(500, f"Error updating lead stage: {str(e)}")