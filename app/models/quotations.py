from app.database import db
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class Quotation(db.Model):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, autoincrement=True)

    document_number = Column(Integer, nullable=False)
    document_name = Column(String, nullable=False)
    total_amount = Column(Numeric(14, 2), nullable=False)
    document_content = Column(String(255), nullable=False)
    summary = Column(String, nullable=False)
    offering_latter = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("document_number", name="uq_quotation_document_number"),
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
    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=True
    )

    contact = relationship("Contact", back_populates="quotations")
    partner = relationship("Partner", back_populates="quotations")
    items = relationship("Item", back_populates="quotation")

    """ Disini buat dict kalau perlu """