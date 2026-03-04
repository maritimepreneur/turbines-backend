from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, String, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.meta.meta import Meta

class GformType(Enum):
    REGISTRATION = "Traning Course Registraion"
    SCHOLARSHIP = "Training Course Scholarship"
    OTHER = "Others"

class Gform(db.Model, Meta):
    _tablename__ = "gform"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    batch = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    type = Column(
        SQLEnum(GformType, name="gform_type_enum"),
        nullable=False
    )
    category = Column(String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "name": self.name,
            "batch": self.batch,
            "date": self.date.isoformat() if self.date else None,
            "type": self.type.value if self.type else None,
            "category": self.category,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }