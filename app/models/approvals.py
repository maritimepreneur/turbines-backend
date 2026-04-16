from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.meta.meta import Meta

class ApprovalStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    LEAVE = "Leave"

class ApprovalType(Enum):
    QUOTATION = "Quotation"
    PO = "Purchase Order"
    INVOICE = "Invoice"
    EXPENSE = "Expense"

class Approval(db.Model, Meta):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(
        SQLEnum(ApprovalStatus, name="approval_status_enum"),
        nullable=True
    )
    type = Column(
        SQLEnum(ApprovalType, name="approval_type_enum"),
        nullable=True
    )
    code = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("code", name="uq_approval_code"),
    )

    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id"),
        nullable=True,
        unique=True
    )
    po_id = Column(
        Integer,
        ForeignKey("purchase_orders.id"),
        nullable=True,
        unique=True
    )
    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=True
    )
    expense_id = Column(
        Integer,
        ForeignKey("expenses.id"),
        nullable=True,
        unique=True
    )

    quotation = relationship("Quotation", back_populates="approval", uselist=False)
    purchase_order = relationship("Purchase_Order", back_populates="approval", uselist=False)
    invoices = relationship("Invoice", back_populates="approvals")
    expense = relationship("Expense", back_populates="approval", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status.value if self.status else None,
            "type": self.type.value if self.type else None,
            "code": self.code,
            "quotation_id": self.quotation_id,
            "po_id": self.po_id,
            "invoice_id": self.invoice_id,
            "expense_id": self.expense_id,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by,
            }
        }
