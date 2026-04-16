from app.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.meta.meta import Meta

class Purchase_Order(db.Model, Meta):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)

    number = Column(String, nullable=False)
    attachments = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("number", name="uq_purchase_order_number"),
    )

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )
    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=True
    )
    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id"),
        nullable=False,
        unique=True
    )

    quotation = relationship("Quotation", back_populates="purchase_order")
    partner = relationship("Partner", back_populates="purchase_orders")
    contact = relationship("Contact", back_populates="purchase_orders")
    invoices = relationship("Invoice", back_populates="purchase_order")
    approval = relationship(
        "Approval",
        back_populates="purchase_order",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "attachments": self.attachments,
            "partner_id": self.partner_id,
            "contact_id": self.contact_id,
            "quotation_id": self.quotation_id,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }
