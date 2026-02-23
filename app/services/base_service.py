from sqlalchemy.orm import Session
from app.utils import response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from enum import Enum as PyEnum
class BaseService:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model
    
    def _inject_create_meta(self, data: dict):
        user_id = self.get_user_id_login()

        data.pop("created_at", None)
        data.pop("updated_at", None)
        data.pop("created_by", None)
        data.pop("updated_by", None)

        data["created_by"] = user_id
        data["updated_by"] = user_id

        return data

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
        data = self._inject_create_meta(data)

        new_obj = self.model(**data)
        self.db.add(new_obj)
        self.db.commit()
        self.db.refresh(new_obj)
        return response(201, "Action Success", new_obj)
    
    def update(self, obj_id, data: dict):
        obj = self._get_by_id(obj_id)
        if not obj:
            return response(404, f"{self.model.__name__} not found")
        
        data.pop("created_at", None)
        data.pop("updated_at", None)
        data.pop("created_by", None)
        data.pop("updated_by", None)
        
        for key, value in data.items():
            setattr(obj, key, value)

        obj.updated_by = self.get_user_id_login()

        self.db.commit()
        self.db.refresh(obj)
        
        return response(200, "Action Success", obj)
    
    def delete(self, obj_id:int):
        obj = self._get_by_id(obj_id)
        if not obj:
            return response(404, f"{self.model.__name__} not found")
        
        self.db.delete(obj)
        self.db.commit()
        return response(200, "Action Success", {"message": f"{self.model.__name__} deleted successfully"})

    def get_user_id_login(self):
        return get_jwt_identity()