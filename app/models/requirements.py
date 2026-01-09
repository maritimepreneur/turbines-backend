from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

class ProjectType(Enum):
    TYPE_0 = "Other"
    TYPE_1 = "BECdex Certification"
    TYPE_2 = "CBEc Training Course"
    TYPE_3 = "Maritime Professional"

class PaymentType(Enum):
    CASH = "Cash"
    CASHLESS = "Cashless"
    DIGITAL = "Digital/Electronic"

class ProjectStage(Enum):
    STAGE_1 = "New Lead"
    STAGE_2 = "Introduction"
    STAGE_3 = "Presentation"
    STAGE_4 = "Proposal"
    STAGE_5 = "Ready to Scale"
    STAGE_6 = "Cancel"

class Requirement(db.Model):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, autoincrement=True)

    project_name = Column(String, nullable=False)
    project_location = Column(String, nullable=False)
    project_type = Column(
        SQLEnum(ProjectType, name="project_type_enum"),
        default=ProjectType.TYPE_0,
        nullable=False
    )
    project_duration = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    payment_type = Column(
        SQLEnum(PaymentType, name="payment_type_enum"),
        default=PaymentType.CASH,
        nullable=False
    )
    project_stage = Column(
        SQLEnum(ProjectStage, name="project_stage_enum"),
        default=ProjectStage.STAGE_1,
        nullable=False
    )
    project_notes = Column(Text, nullable=True)
    attachment_name = Column(String(255), nullable=False)
    attachment_path = Column(String(255), nullable=False)
    attachment_type = Column(String)
    attachment_size = Column(Integer)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=True
    )
    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )

    customer = relationship("Customer", back_populates="requirements")
    partner = relationship("Partner", back_populates="requirements")

    """ Disini buat dict kalau perlu """