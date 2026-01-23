from database import db
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

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )
    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=True
    ),
    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=True
    )

    """ Disini buat dict kalau perlu """