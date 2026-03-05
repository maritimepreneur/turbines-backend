from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.services.base_service import BaseService
from app.models.specialization import Specialization
from app.utils import response

class SpecializationService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Specialization)
    
    def get_all_specializations(self):
        try:
            specializations = self.db.query(Specialization).all()
            data = [spec.to_dict() for spec in specializations]
            return response(200, "Action Success", data)
        except Exception as e:
            return response(500, f"Error fetching specializations: {str(e)}")
    
    def get_specialization_by_id(self, specialization_id: int):
        return self.get_by_id(specialization_id)
    
    def create_specialization(self, data):
        try:
            # Validasi code unique
            existing = self.db.query(Specialization).filter(Specialization.code == data.get('code')).first()
            if existing:
                return response(400, f"Specialization with code '{data.get('code')}' already exists")
            
            return self.create(data)
        except Exception as e:
            return response(500, f"Error creating specialization: {str(e)}")
    
    def update_specialization(self, specialization_id: int, data):
        try:
            # Validasi code unique (exclude current record)
            if 'code' in data:
                existing = self.db.query(Specialization).filter(
                    Specialization.code == data.get('code'),
                    Specialization.id != specialization_id
                ).first()
                if existing:
                    return response(400, f"Specialization with code '{data.get('code')}' already exists")
            
            return self.update(specialization_id, data)
        except Exception as e:
            return response(500, f"Error updating specialization: {str(e)}")
    
    def delete_specialization(self, specialization_id: int):
        return self.delete(specialization_id)

    def get_specialization_list_filter(self, payload):
        """Get specializations with filter and pagination"""
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')
            
            query = self.db.query(Specialization)
            
            if search_query:
                query = query.filter(
                    or_(
                        Specialization.name.ilike(f"%{search_query}%"),
                        Specialization.code.ilike(f"%{search_query}%"),
                        Specialization.description.ilike(f"%{search_query}%")
                    )
                )
            
            if hasattr(Specialization, sort_by):
                sort_column = getattr(Specialization, sort_by)
            else:
                sort_column = Specialization.id
            
            if sort_order.upper() == 'DESC':
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
            
            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            
            raw_data = query.offset(offset).limit(page_size).all()
            data = [spec.to_dict() for spec in raw_data]
            
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
            return response(500, f"Error filtering specializations: {str(e)}")