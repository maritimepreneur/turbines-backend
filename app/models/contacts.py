from app.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.models.meta.meta import Meta

class Contact(db.Model, Meta):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    emails = Column(JSONB, nullable=False, default=list, server_default="[]")
    phone_numbers = Column(JSONB, nullable=False, default=list, server_default="[]")
    company = Column(String, nullable=False)
    agreement_id = Column(Integer, ForeignKey("agreements.id"))
    nasionality = Column(String, nullable=True)
    role = Column(String, nullable=True)

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )

    __table_args__ = (
        UniqueConstraint("emails", name="uq_contact_emails"),
        UniqueConstraint("phone_numbers", name="uq_contact_phone_numbers"),
    )

    leads = relationship("Lead", back_populates="contact")
    quotations = relationship("Quotation", back_populates="contact")
    purchase_orders = relationship("Purchase_Order", back_populates="contact")
    invoices = relationship("Invoice", back_populates="contact")
    projects = relationship("Project", back_populates="contact")
    agreement = relationship("Agreement", back_populates="contacts")
    contact_partners = relationship("ContactPartner", back_populates="contact")
    partners = relationship("Partner", secondary="contact_partners", viewonly=True)

    def to_dict(self):
        """
        Helper method untuk mengubah object SQLAlchemy menjadi Dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "emails": self.emails,
            "phone_numbers": self.phone_numbers,
            "company": self.company,
            "role": self.role,
            "position": self.position,
            "partners": [p.to_dict() for p in self.partners] if self.partners else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by
        }
        
    @property
    def partners(self):
        return [cp.partner for cp in self.contact_partners]