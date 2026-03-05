from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, String, Date, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.meta.meta import Meta

class ScholarshipStatus(Enum):
    ACTIVE = "Active"
    DEACTIVE = "Deactive"

class Scholarship(db.Model, Meta):
    __tablename__ = "scholarship"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    status = Column (
        SQLEnum(ScholarshipStatus, name="sholarship_status_enum"),
        nullable=False
    )
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    original_price = Column(Numeric(14, 2), nullable=False)
    discount = Column(Integer, nullable=False)
    price = Column(Numeric(14, 2), nullable=False)
    code = Column(String, nullable=False)

    registration = relationship("Registration", back_populates="scholarship")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value if self.status else None,
            "date": self.date.isoformat() if self.date else None,
            "type": self.type,
            "category": self.category,
            "original_price": self.original_price,
            "discount": self.discount,
            "price": self.price,
            "code": self.code,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }