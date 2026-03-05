from app.database import db
from sqlalchemy import Column, Integer, DATE, Numeric, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.meta.meta import Meta

class Payment(db.Model, Meta):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DATE, nullable=False)
    code = Column(String, nullable=False)
    nominal = Column(Numeric(14, 2), nullable=False)
    notes = Column(Text, nullable=False)
    attachments = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("code", name="uq_payment_code"),
    )

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=True
    )

    registration_id = Column(
        Integer,
        ForeignKey("registration.id"),
        nullable=True
    )

    invoice = relationship("Invoice", back_populates="payments")
    registration = relationship("Registration", back_populates="payments")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "code": self.code,
            "nominal": float(self.nominal),
            "notes": self.notes,
            "attachments": self.attachments,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }