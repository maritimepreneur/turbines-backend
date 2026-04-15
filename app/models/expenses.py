from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, DATE, String, Numeric, Text, Enum as SQLEnum, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from app.models.meta.meta import Meta

class ExpenseStatus(Enum):
    DRAFT = "Draft"
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PAID = "Paid"
    CANCELED = "Canceled"

class Expense(db.Model, Meta):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    period_date = Column(DATE, nullable=False)
    code = Column(String, nullable=False)
    status = Column(
        SQLEnum(ExpenseStatus, name="expense_status_enum"),
        default=ExpenseStatus.DRAFT,
        nullable=False
    )
    total_amount = Column(Numeric(14, 2), nullable=False)
    notes = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("code", name="uq_expense_code"),
    )

    approval = relationship("Approval", back_populates="expense", uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "period_date": self.period_date.isoformat() if self.period_date else None,
            "code": self.code,
            "status": self.status.value if self.status else None,
            "total_amount": str(self.total_amount),
            "notes": self.notes,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }