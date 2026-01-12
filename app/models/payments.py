from app.database import db
from sqlalchemy import Column, Integer, DATE, Numeric, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class Payment(db.Model):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DATE, nullable=False)
    nominal = Column(Numeric(14, 2), nullable=False)
    notes = Column(Text, nullable=False)
    attachments = Column(String, nullable=False)

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=True
    )
    po_id = Column(
        Integer,
        ForeignKey("purchase_orders.id"),
        nullable=True
    )

    invoice = relationship("Invoice", back_populates="payments")
    purchase_order = relationship("Purchase_Order", back_populates="payments")

    """" Disini buat dict kalau perlu """