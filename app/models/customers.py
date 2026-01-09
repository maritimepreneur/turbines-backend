from app.database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Customer(db.Model):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)

    users = relationship("User", back_populates="customer")
    requirements = relationship("Requirement", back_populates="customer")
    quotations = relationship("Quotation", back_populates="customer")
    purchase_orders = relationship("Purchase_Order", back_populates="customer")
    invoices = relationship("Invoice", back_populates="customer")