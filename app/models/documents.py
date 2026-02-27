from app.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, UniqueConstraint
from enum import Enum
from sqlalchemy.orm import relationship
from app.models.meta.meta import Meta

class DocumentType(Enum):
    OTHER = "Other Document"
    RECOMENDATION = "Recomendation Letter"
    PO = "Puchase Order"
    INVOICE = "Invoice"
    MOU = "MoU"
    TAX = "Tax"
    REPORT = "Report"
    CERTIFICATE = "Certificate"
    AGREEMENT = "Agreement"
    QUOTATION = "Quotation"
    PROPOSAL = "Proposal"

class Document(db.Model, Meta):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String, nullable=False)
    name = Column(String, nullable=False)
    document_type = Column(
        SQLEnum(DocumentType, name="documen_type_enum"),
        default=DocumentType.OTHER,
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("number", name="uq_document_code"),
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=True
    )
    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id"),
        nullable=True
    )

    project = relationship("Project", back_populates="documents")
    quotation = relationship("Quotation", back_populates="documents")
    agreement = relationship("Agreement", back_populates="documents")


    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "name": self.name,
            "document_type": self.document_type.value if self.document_type else None,
            "project_id": self.project_id,
            "quotation_id": self.quotation_id,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }