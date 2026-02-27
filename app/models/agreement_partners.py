from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import db

class AgreementPartner(db.Model):
    __tablename__ = "agreement_partners"

    agreement_id = Column(Integer, ForeignKey("agreements.id"), primary_key=True)
    partner_id = Column(Integer, ForeignKey("partners.id"), primary_key=True)

    agreement = relationship("Agreement", back_populates="agreement_partners")
    partner = relationship("Partner", back_populates="agreement_partners")