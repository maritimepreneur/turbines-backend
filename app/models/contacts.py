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

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )

    __table_args__ = (
        UniqueConstraint("emails", name="uq_contact_emails"),
        UniqueConstraint("phone_numbers", name="uq_contact_phone_numbers"),
    )

    partner = relationship("Partner", back_populates="contacts")
    leads = relationship("Lead", back_populates="contact")
    quotations = relationship("Quotation", back_populates="contact")
    purchase_orders = relationship("Purchase_Order", back_populates="contact")
    invoices = relationship("Invoice", back_populates="contact")
    projects = relationship("Project", back_populates="contact")
    agreement = relationship("Agreement", back_populates="contacts")

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
            "partner_id": self.partner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by
        }
        
    """" Disini buat dict kalau perlu """
