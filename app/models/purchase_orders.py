from app.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class Purchase_Order(db.Model):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)

    number = Column(String(100), unique=True, nullable=False)
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
        nullable=True
    )

    quotation = relationship("Quotation", back_populates="purchase_orders")
    partner = relationship("Partner", back_populates="purchase_orders")
    contact = relationship("Contact", back_populates="purchase_orders")
    invoices = relationship("Invoice", back_populates="purchase_order")
    approvals = relationship("Approval", back_populates="purchase_orders")

    """ Disini buat dict kalau perlu """
    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "attachments": self.attachments,
            "partner_id": self.partner_id,
            "contact_id": self.contact_id,
            "quotation_id": self.quotation_id
        }