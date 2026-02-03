from app.database import db
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class Quotation(db.Model):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, autoincrement=True)

    total_amount = Column(Numeric(14, 2), nullable=False)
    document_content = Column(String(255), nullable=False)
    summary = Column(String, nullable=False)
    offering_letter = Column(String, nullable=False)

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
    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=True
    )

    lead = relationship("Lead", back_populates="quotations")
    contact = relationship("Contact", back_populates="quotations")
    partner = relationship("Partner", back_populates="quotations")
    purchase_orders = relationship("Purchase_Order", back_populates="quotation")
    approvals = relationship("Approval", back_populates="quotations")
    items = relationship("Item", back_populates="quotation")
    documents = relationship("Document", back_populates="quotation")

    """ Disini buat dict kalau perlu """