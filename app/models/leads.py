from app.database import db
from sqlalchemy import Column, Integer, String, Text, DATE, ForeignKey
from sqlalchemy.orm import relationship

class Lead(db.Model):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    period = Column(DATE, nullable=False)
    description = Column(Text, nullable=False)

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=True
    )
    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )

    contact = relationship("Contact", back_populates="leads")
    partner = relationship("Partner", back_populates="leads")
    projects = relationship("Project", back_populates="lead")

    """" Disini buat dict kalau perlu """