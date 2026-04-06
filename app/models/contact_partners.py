from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import db
from app.models.meta.meta import Meta

class ContactPartner(db.Model, Meta):
    __tablename__ = "contact_partners"

    contact_id = Column(Integer, ForeignKey("contacts.id"), primary_key=True)
    partner_id = Column(Integer, ForeignKey("partners.id"), primary_key=True)

    contact = relationship("Contact", back_populates="contact_partners")
    partner = relationship("Partner", back_populates="contact_partners")