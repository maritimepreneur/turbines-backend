from database import db
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class Purchase_Order(db.Model):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)

    number = Column(Integer, nullable=False)
    attachments = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("number", name="uq_purchase_order_number"),
    )

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=False
    )
    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=False
    )

    partner = relationship("Partner", back_populates="purchase_orders")
    contact = relationship("Contact", back_populates="purchase_orders")
    invoices = relationship("Invoice", back_populates="purchase_order")
    payments = relationship("Payment", back_populates="purchase_order")

    """ Disini buat dict kalau perlu """