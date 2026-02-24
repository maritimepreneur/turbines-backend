from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import db

class Requirement(db.Model):
    __tablename__ = "requirements"

    id = Column (Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    code = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("code", name="uq_requirement_code"),
    )

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )

    partners = relationship("Partner", back_populates="requirements")
    cv_trackers = relationship("CV_Tracker", back_populates="requirement")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "partner_id": self.partner_id
        }