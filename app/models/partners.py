from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.models.meta.meta import Meta

class CompanyType(Enum):
    OTHER = "Other"
    GOVERMENT = "Goverment"
    PRIVATE = "Private"
    STATEOWNED = "State Owned"
    PUBLIC = "Public"
    NONPROFIT = "Non-Profit"

class PartnerType(Enum):
    VENDOR = "Vendor"
    CLIENT = "Client"
    UNCATEGORIED = "Uncategorized"
    BOTH = "Both"

class Partner(db.Model, Meta):
    __tablename__= "partners"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    initials = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    company_type = Column(
        SQLEnum(CompanyType, name="company_type_enum"),
        default=CompanyType.OTHER,
        nullable=False
    )
    partner_type = Column(
        SQLEnum(PartnerType, name="partner_type_enum"),
        nullable=False
    )
    service = Column(JSONB, nullable=True, default=list, server_default="[]")
    goods = Column(JSONB, nullable=True, default=list, server_default="[]")

    leads = relationship("Lead", back_populates="partner")
    projects = relationship("Project", back_populates="partner")
    quotations = relationship("Quotation", back_populates="partner")
    purchase_orders = relationship("Purchase_Order", back_populates="partner")
    invoices = relationship("Invoice", back_populates="partner")
    requirements = relationship("Requirement", back_populates="partners")
    agreement_partners = relationship("AgreementPartner", back_populates="partner")
    contact_partners = relationship("ContactPartner", back_populates="partner")
    contacts = relationship("Contact", secondary="contact_partners", viewonly=True)

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
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }
