from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

class ProjectType(Enum):
    OTHER = "Other"
    BECDEX = "BECdex Certification"
    CBEC = "CBEc Training Course"
    MARITIME = "Maritime Professional"

class PaymentType(Enum):
    CASH = "Cash"
    CASHLESS = "Cashless"
    DIGITAL = "Digital/Electronic"

class Stages(Enum):
    CONCEPT = "Concept"
    PLANNING = "Planning"
    EXECUTION = "Execution"
    MONITORING = "Monitoring"
    CLOSING = "Closing"

class Project(db.Model):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    type = Column(
        SQLEnum(ProjectType, name="project_type_enum"),
        default=ProjectType.OTHER,
        nullable=False
    )
    duration = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    payment_type = Column(
        SQLEnum(PaymentType, name="payment_type_enum"),
        default=PaymentType.CASH,
        nullable=False
    )
    description = Column(Text, nullable=False)
    current_stages = Column(
        SQLEnum(Stages, name="project_stages_enum"),
        default=Stages.CONCEPT,
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
    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=True
    )
    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=True
    )

    contact = relationship("Contact", back_populates="projects")
    partner = relationship("Partner", back_populates="projects")
    invoices = relationship("Invoice", back_populates="projects")
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    lead = relationship("Lead", back_populates="projects")

    """ Disini buat dict kalau perlu """