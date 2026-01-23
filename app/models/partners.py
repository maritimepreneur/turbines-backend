from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

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
    industry = Column(String, nullable=False)
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
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="partner")
    contacts = relationship("Contact", back_populates="partner")
    leads = relationship("Lead", back_populates="partner")
    projects = relationship("Project", back_populates="partner")
    quotations = relationship("Quotation", back_populates="partner")
    purchase_orders = relationship("Purchase_Order", back_populates="partner")
    invoices = relationship("Invoice", back_populates="partner")

    def to_dict(self):
        """ Helper untuk mengubah object SQLAlchemy menjadi Dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "initials": self.initials,
            "industry": self.industry,
            "company_type": self.company_type.value if self.company_type else None,
            "partner_type": self.partner_type.value if self.partner_type else None,
            "service": self.service,
            "goods": self.goods,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

""" Disini buat dict kalau perlu """