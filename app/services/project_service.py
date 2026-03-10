from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from datetime import datetime
from app.models.projects import Project, ProjectType, PaymentType, Stages
from app.models.contacts import Contact
from app.models.partners import Partner
from app.models.leads import Lead
from app.models.invoices import Invoice
from app.services.base_service import BaseService
from app.utils import response

class ProjectService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Project)

    def get_all_projects(self):
        """ Get all Projects """
        projects = self.db.query(Project).all()
        data = [p.to_dict() for p in projects]
        return response(200, "Success", data)
    
    def create_project(self, data):
        """ Create a new project """
        validation = self.validate_fk(data)
        if validation: return validation

        try:
            if 'type' in data: 
                data['type'] = ProjectType(data['type'])
            if 'payment_type' in data: 
                data['payment_type'] = PaymentType(data['payment_type'])
            if 'current_stages' in data: 
                data['current_stages'] = Stages(data['current_stages'])
        except ValueError as e:
            return response(400, f"Invalid enum value provided. Ensure the exact text matches the options.")

        date_str = datetime.now().strftime("%d%m%y")
        
        lead_id = data.get('lead_id')
        lead_str = str(lead_id) if lead_id else "000"
        
        data['code'] = f"MMN-{date_str}-{lead_str}"

        existing_code = self.db.query(Project).filter(Project.code == data.get('code')).first()
        if existing_code:
            return response(400, f"Project code {data['code']} already exists")
            
        return super().create(data)
    
    def get_project_by_id(self, project_id):
        """ Get Project details """
        project = self._get_by_id(project_id)
        if not project:
            return response(404, "Project not found", None)
        return response(200, "Success", project.to_dict())
    
    def update_project_by_id(self, project_id, data):
        """ Update Project """
        project = self._get_by_id(project_id)
        if not project:
            return response(404, f"Project ID {project_id} not found")
            
        validation = self.validate_fk(data)
        if validation: return validation

        try:
            if 'type' in data: 
                data['type'] = ProjectType(data['type'])
            if 'payment_type' in data: 
                data['payment_type'] = PaymentType(data['payment_type'])
            if 'current_stages' in data: 
                data['current_stages'] = Stages(data['current_stages'])
        except ValueError as e:
            return response(400, f"Invalid enum value provided. Ensure the exact text matches the options.")

        if 'code' in data and data['code'] != project.code:
            existing = self.db.query(Project).filter(Project.code == data['code']).first()
            if existing:
                return response(400, "Project code already exists")

        return super().update(project_id, data)
    
    def validate_fk(self, data):
        """ Validation logic for Foreign Keys """
        if data.get("contact_id") and not self.db.get(Contact, data["contact_id"]):
            return response(404, "Invalid contact_id")
        
        if data.get("partner_id") and not self.db.get(Partner, data["partner_id"]):
            return response(404, "Invalid partner_id")
        
        if data.get("lead_id") and not self.db.get(Lead, data["lead_id"]):
            return response(404, "Invalid lead_id")
            
        if data.get("invoice_id") and not self.db.get(Invoice, data["invoice_id"]):
            return response(404, "Invalid invoice_id")

        return None

    def get_project_list_filter(self, payload):
        """ Search, Filter, and Pagination for Projects """
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')
            project_type = payload.get('type')
            current_stage = payload.get('current_stages')
            start_date = payload.get('start_date')
            end_date = payload.get('end_date')

            query = self.db.query(Project)\
                .outerjoin(Partner, Project.partner_id == Partner.id)\
                .outerjoin(Contact, Project.contact_id == Contact.id)

            if search_query:
                query = query.filter(
                    or_(
                        Project.name.ilike(f"%{search_query}%"),
                        Project.code.ilike(f"%{search_query}%"),
                        Project.location.ilike(f"%{search_query}%"),
                        Project.description.ilike(f"%{search_query}%")
                    )
                )

            if project_type:
                try:
                    query = query.filter(Project.type == ProjectType(project_type))
                except ValueError:
                    pass
                    
            if current_stage:
                try:
                    query = query.filter(Project.current_stages == Stages(current_stage))
                except ValueError:
                    pass
            # ---------------------------
            
            if start_date and end_date:
                query = query.filter(Project.start_date.between(start_date, end_date))
            elif start_date:
                query = query.filter(Project.start_date >= start_date)

            sort_column = getattr(Project, sort_by) if hasattr(Project, sort_by) else Project.id
            query = query.order_by(desc(sort_column) if sort_order.upper() == 'DESC' else asc(sort_column))
            
            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            raw_data = query.offset(offset).limit(page_size).all()
            
            data_list = []
            for p in raw_data:
                item = p.to_dict()
                item["partner_name"] = p.partner.name if p.partner else None
                item["contact_name"] = p.contact.name if p.contact else None
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
            return response(500, f"Error processing project filter: {str(e)}")