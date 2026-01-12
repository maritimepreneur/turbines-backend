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

class Project(db.Model):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    type = Column(
        SQLEnum(ProjectType, name="project_type_enum"),
        default=ProjectType.TYPE_0,
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

    customer = relationship("Contact", back_populates="projects")
    partner = relationship("Partner", back_populates="projects")
    stages = relationship("Stage", back_populates="project")

    """ Disini buat dict kalau perlu """