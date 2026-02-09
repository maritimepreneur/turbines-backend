from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

class ApprovalType(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class Approval(db.Model):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(
        SQLEnum(ApprovalType, name="approval_type_enum"),
        nullable=False
    )
    code = Column(Integer, nullable=False)

    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id"),
        nullable=True
    )
    po_id = Column(
        Integer,
        ForeignKey("purchase_orders.id"),
        nullable=True
    )
    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=True
    )
    expense_id = Column(
        Integer,
        ForeignKey("expenses.id"),
        nullable=True
    )

    quotations = relationship("Quotation", back_populates="approvals")
    purchase_orders = relationship("Purchase_Order", back_populates="approvals")
    invoices = relationship("Invoice", back_populates="approvals")
    expense = relationship("Expense", back_populates="approvals")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type.value if self.type else None,
            "code": self.code,
            "quotation_id": self.quotation_id,
            "po_id": self.po_id,
            "invoice_id": self.invoice_id,
            "expense_id": self.expense_id
        }