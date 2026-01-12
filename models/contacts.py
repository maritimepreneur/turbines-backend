from database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Contact(db.Model):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    company = Column(String, nullable=False)

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )

    partner = relationship("Partner", back_populates="contacts")
    leads = relationship("Lead", back_populates="contact")
    quotations = relationship("Quotation", back_populates="contact")
    purchase_orders = relationship("Purchase_Order", back_populates="contact")
    invoices = relationship("Invoice", back_populates="contact")
    projects = relationship("Project", back_populates="customer")

    """" Disini buat dict kalau perlu """