from app.database import db
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.meta.meta import Meta

class Quotation(db.Model, Meta):
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
    items = relationship("Item", back_populates="quotation", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="quotation")

    def to_dict(self):
        return {
            "id": self.id,
            "total_amount": str(self.total_amount),
            "document_content": self.document_content,
            "summary": self.summary,
            "offering_letter": self.offering_letter,
            "contact_id": self.contact_id,
            "partner_id": self.partner_id,
            "lead_id": self.lead_id,
            "item": {
                "name": self.items.name,
                "cost": self.items.cost,
                "amount": self.items.amount,
                "billed_amount": self.items.billed_amount,
                "type": self.items.type,
                "amount_type": self.items.amount_type,
                "attachments": self.items.attachments
            },
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }