from app.database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.meta.meta import Meta

class Specialization(db.Model, Meta):
    __tablename__ = "specialization"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    code = Column(String, nullable=False)

    registration = relationship("Registration", back_populates="specialization")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "code": self.code,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }