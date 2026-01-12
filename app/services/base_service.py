from sqlalchemy.orm import Session
from app.utils import response

class BaseService:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def get_all(self):
        return response(200, "Action Success", self.db.query(self.model).all())
    
    def get_by_id(self, obj_id: int):
        _data = self.db.query(self.model).filter(self.model.id == obj_id).first()
        if not _data :
            return response(404, "Not Found")
        return response(200, "Action Success", _data)
    
    def _get_by_id(self, obj_id: int):
        return self.db.query(self.model).filter(self.model.id == obj_id).first()
    
    def create(self, data):
        new_obj = self.model(**data)
        self.db.add(new_obj)
        self.db.commit()
        self.db.refresh(new_obj)
        return response(200, "Action Success", new_obj)
    
    def update(self, obj_id, data):
        obj = self._get_by_id(obj_id)
        if not obj:
            return response(404, f"{self.model.__name__} not found")
        
        for key, value in data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return response(200, "Action Success", obj)
    
    def delete(self, obj_id:int):
        obj = self._get_by_id(obj_id)
        if not obj:
            raise response(404, f"{self.model.__name__} not found")
        
        self.db.delete(obj)
        self.db.commit()
        return response(200, "Action Success", {"message": f"{self.model.__name__} deleted successfully"})