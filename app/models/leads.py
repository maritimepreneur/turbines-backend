from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DATE, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

class Stages(Enum):
    NEW = "New Lead"
    INTRODUCTION = "Introduction"
    PRESENTATION = "Presentation"
    QUOTATION = "Quotation"
    FU = "Follow Up"
    MOU = "MoU"
    EXECUTION = "Execution"

class Lead(db.Model):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    period = Column(DATE, nullable=False)
    description = Column(Text, nullable=False)
    attachments = Column(JSONB, nullable=False, default=list, server_default="[]")
    current_stages = Column(
        SQLEnum(Stages, name="lead_stages_enum"),
        default=Stages.NEW,
        nullable=False
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

    # Relationships
    contact = relationship("Contact", back_populates="leads")
    partner = relationship("Partner", back_populates="leads")
    projects = relationship("Project", back_populates="lead")
    quotations = relationship("Quotation", back_populates="lead")

    def to_dict(self):
        """ Helper to convert SQLAlchemy object to Dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "period": self.period.isoformat() if self.period else None,
            "description": self.description,
            "contact_id": self.contact_id,
            "partner_id": self.partner_id,
            "current_stages": self.current_stages.name if self.current_stages else None,  
            # Flatten nested data for display if needed
            "contact_name": self.contact.name if self.contact else None,
            "company": self.contact.company if self.contact else None, # Company comes from Contact
            "partner_name": self.partner.name if self.partner else None
        }