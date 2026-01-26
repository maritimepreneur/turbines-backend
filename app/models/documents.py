from app.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from enum import Enum
from sqlalchemy.orm import relationship

class DocumentType(Enum):
    OTHER = "Other Document"
    RECOMENDATION = "Recomendation Letter"
    PO = "Puchase Order"
    INVOICE = "Invoice"
    MOU = "MoU"
    TAX = "Tax"
    REPORT = "Report"
    CERTIFICATE = "Certificate"
    AGGREMENT = "Agreement"

class Document(db.Model):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    document_type = Column(
        SQLEnum(DocumentType, name="documen_type_enum"),
        default=DocumentType.OTHER,
        nullable=False
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=True
    )

    # Relationships
    project = relationship("Project", back_populates="documents")

    """ Disini buat dict kalau perlu """