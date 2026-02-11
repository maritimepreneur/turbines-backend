from app.database import db
from sqlalchemy import Column, Integer, DATE, String, Numeric, Text
from sqlalchemy.orm import relationship

class Expense(db.Model):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    period_date = Column(DATE, nullable=False)
    code = Column(String, nullable=False)
    status = Column(String, nullable=False)
    total_amount = Column(Numeric(14, 2), nullable=False)
    notes = Column(Text, nullable=False)

    items = relationship("Item", back_populates="expense")
    approvals = relationship("Approval", back_populates="expense")

    def to_dict(self):
        return {
            "id": self.id,
            "period_date": self.period_date.isoformat() if self.period_date else None,
            "code": self.code,
            "status": self.status,
            "total_amount": str(self.total_amount),
            "notes": self.notes
        }