from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import db
from sqlalchemy.dialects.postgresql import JSONB
from app.models.meta.meta import Meta

class Agreement(db.Model, Meta):
    __tablename__ = "agreements"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    contact_ids = Column(JSONB, nullable=False, default=list, server_default="[]")

    contacts = relationship("Contact", back_populates="agreement")
    documents = relationship("Document", back_populates="agreement")
    agreement_partners = relationship("AgreementPartner", back_populates="agreement")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "contact_ids": self.contact_ids if self.contact_ids else [],
            "document": {
                "id": self.documents.id,
                "number": self.documents.number,
                "name": self.documents.name,
                "document_type": self.documents.document_type
            } if self.documents else None,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }