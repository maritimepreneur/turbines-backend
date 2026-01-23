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
    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=True
    )
    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id"),
        nullable=True,
    )
    po_id = Column(
        Integer,
        ForeignKey("purchase_orders.id"),
        nullable=True
    )

    contact = relationship("Contact", back_populates="leads")
    partner = relationship("Partner", back_populates="leads")
    projects = relationship("Project", back_populates="lead")
    documents = relationship("Document", back_populates="lead")

    """" Disini buat dict kalau perlu """