from database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Partner(db.Model):
    __tablename__= "partners"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)

    users = relationship("User", back_populates="partner")
    requirements = relationship("Requirement", back_populates="partner")
    quotations = relationship("Quotation", back_populates="partner")
    purchase_orders = relationship("Purchase_Order", back_populates="partner")
    invoices = relationship("Invoice", back_populates="partner")

    """ Disini buat dict kalau perlu """