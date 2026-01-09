from app.database import db
from sqlalchemy import Column, Integer, Numeric, Text, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Invoice(db.Model):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True)

    number = Column(Integer, nullable=False)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    period = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    billed_amount = Column(Numeric(14, 2), nullable=False)
    total_amount = Column(Numeric(14, 2), nullable=False)
    notes = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("number", name="uq_invoice_number"),
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=True
    )
    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )
    purchase_order_id = Column(
        Integer,
        ForeignKey("purchase_orders.id"),
        nullable=True
    )

    customer= relationship("Customer", back_populates="invoices")
    partner= relationship("Partner", back_populates="invoices")
    purchase_order = relationship("Purchase_Order", back_populates="invoices")

    """" Disini buat dict kalau perlu """