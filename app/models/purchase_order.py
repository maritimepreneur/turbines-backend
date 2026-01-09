from database import db
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class Purchase_Order(db.Model):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)

    po_number = Column(Integer, nullable=False)
    total_amount = Column(Numeric(14, 2), nullable=False)
    attachment_name = Column(String(255), nullable=False)
    attachment_path = Column(String(255), nullable=False)
    attachment_type = Column(String)
    attachment_size = Column(Integer)

    __table_args__ = (
        UniqueConstraint("po_number", name="uq_purchase_order_po_number"),
    )

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=False
    )
    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    partner = relationship("Partner", back_populates="purchase_orders")
    customer = relationship("Customer", back_populates="purchase_orders")
    invoices = relationship("Invoice", back_populates="purchase_order")

    """ Disini buat dict kalau perlu """