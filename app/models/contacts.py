from app.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

class Contact(db.Model):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    emails = Column(JSONB, nullable=False, default=list, server_default="[]")
    phone_numbers = Column(JSONB, nullable=False, default=list, server_default="[]")
    company = Column(String, nullable=False)

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )
    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
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

    """" Disini buat dict kalau perlu """