from app.database import db
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

class Item(db.Model):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cost = Column(Numeric(14, 2), nullable=False)
    amount = Column(Numeric(14, 2), nullable=False)
    billed_amount = Column(Numeric(14, 2), nullable=False)
    type = Column(String, nullable=False)
    amount_type = Column(String, nullable=False)
    attachments = Column(JSONB, nullable=False, default=list, server_default="[]")

    expense_id = Column(
        Integer,
        ForeignKey("expenses.id"),
        nullable=True
    )
    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id"),
        nullable=True
    )
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

    expense = relationship("Expense", back_populates="items")
    quotation = relationship("Quotation", back_populates="items")

    """" Disini buat dict kalau perlu """