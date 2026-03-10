from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.models.gform import Gform, GformType
from app.services.base_service import BaseService
from app.utils import response

class GformService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Gform)

    def get_all_gforms(self):
        """ Get all Gforms """
        gforms = self.db.query(Gform).all()
        data = [g.to_dict() for g in gforms]
        return response(200, "Success", data)
    
    def create_gform(self, data):
        """ Create a new Gform """
        try:
            if 'type' in data: 
                data['type'] = GformType(data['type'])
        except ValueError:
            return response(400, "Invalid Gform type provided.")
            
        return super().create(data)
    
    def get_gform_by_id(self, gform_id):
        """ Get Gform details by ID """
        gform = self._get_by_id(gform_id)
        if not gform:
            return response(404, "Gform not found", None)
        return response(200, "Success", gform.to_dict())
    
    def update_gform_by_id(self, gform_id, data):
        """ Update Gform """
        gform = self._get_by_id(gform_id)
        if not gform:
            return response(404, f"Gform ID {gform_id} not found")

        try:
            if 'type' in data: 
                data['type'] = GformType(data['type'])
        except ValueError:
            return response(400, "Invalid Gform type provided.")

        return super().update(gform_id, data)

    def get_gform_list_filter(self, payload):
        """ Search, Filter, and Pagination for Gforms """
        try:
            page_size = payload.get('page_size', 25)
            page_number = payload.get('page_number', 1)
            sort_by = payload.get('sort_by', 'id')
            sort_order = payload.get('sort_order', 'DESC')
            search_query = payload.get('search', '')
            gform_type = payload.get('type')
            batch = payload.get('batch')

            query = self.db.query(Gform)

            if search_query:
                query = query.filter(
                    or_(
                        Gform.name.ilike(f"%{search_query}%"),
                        Gform.category.ilike(f"%{search_query}%")
                    )
                )

            if gform_type:
                try:
                    query = query.filter(Gform.type == GformType(gform_type))
                except ValueError:
                    pass
            
            if batch is not None:
                query = query.filter(Gform.batch == batch)

            sort_column = getattr(Gform, sort_by) if hasattr(Gform, sort_by) else Gform.id
            query = query.order_by(desc(sort_column) if sort_order.upper() == 'DESC' else asc(sort_column))
            
            total_items = query.count()
            total_pages = (total_items + page_size - 1) // page_size
            offset = (page_number - 1) * page_size
            raw_data = query.offset(offset).limit(page_size).all()
            
            data_list = [g.to_dict() for g in raw_data]

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
            return response(500, f"Error processing gform filter: {str(e)}")