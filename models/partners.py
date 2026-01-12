from database import db
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship

class CompanyType(Enum):
    TYPE_0 = "Other"
    TYPE_1 = "Goverment"
    TYPE_2 = "Private"
    TYPE_3 = "State Owned"
    TYPE_4 = "Public"
    TYPE_5 = "Non-Profit"

class PartnerType(Enum):
    VENDOR = "Vendor"
    CLIENT = "Client"
    BOTH = "Both"

class Partner(db.Model):
    __tablename__= "partners"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    initials = Column(String, nullable=False)
    industrials = Column(String, nullable=False)
    company_type = Column(
        SQLEnum(CompanyType, name="company_type_enum"),
        default=CompanyType.TYPE_0,
        nullable=False
    )
    partner_type = Column(
        SQLEnum(PartnerType, name="partner_type_enum"),
        nullable=False
    )
    service = Column(String, nullable=True)
    goods = Column(String, nullable=True)

    users = relationship("User", back_populates="partner")
    contacts = relationship("Contact", back_populates="partner")
    leads = relationship("Lead", back_populates="partner")
    projects = relationship("Project", back_populates="partner")
    quotations = relationship("Quotation", back_populates="partner")
    purchase_orders = relationship("Purchase_Order", back_populates="partner")
    invoices = relationship("Invoice", back_populates="partner")

    """ Disini buat dict kalau perlu """