from app.database import db
from sqlalchemy import Column, String, Integer, Numeric, Text, Date, DateTime, ForeignKey, UniqueConstraint
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
    vat = Column(Numeric(14, 2), nullable=False)
    pph = Column(Numeric(14, 2), nullable=False)
    overheads = Column(Numeric(14, 2), nullable=False)
    discount = Column(Numeric(14, 2), nullable=False)
    grand_total = Column(Numeric(14, 2), nullable=False)
    payment_details = Column(Text, nullable=False)
    agreement_letter = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("number", name="uq_invoice_number"),
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
    purchase_order_id = Column(
        Integer,
        ForeignKey("purchase_orders.id"),
        nullable=True
    )

    contact = relationship("Contact", back_populates="invoices")
    partner = relationship("Partner", back_populates="invoices")
    purchase_order = relationship("Purchase_Order", back_populates="invoices")
    payments = relationship("Payment", back_populates="invoice")
    approvals = relationship("Approval", back_populates="invoices")
    projects = relationship("Project", back_populates="invoices")

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "created": self.created.isoformat() if self.created else None,
            "period": self.period.isoformat() if self.period else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "billed_amount": float(self.billed_amount),
            "total_amount": float(self.total_amount),
            "notes": self.notes,
            "vat": float(self.vat),
            "pph": float(self.pph),
            "overheads": float(self.overheads),
            "discount": float(self.discount),
            "grand_total": float(self.grand_total),
            "payment_details": float(self.payment_details),
            "agreement_letter": self.agreement_letter,
            "contact_id": self.contact_id,
            "partner_id": self.partner_id,
            "purchase_order_id": self.purchase_order_id
        }