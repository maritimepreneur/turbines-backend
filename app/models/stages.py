from database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Stage(db.Model):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    attachments = Column(String, nullable=False)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=True
    )
    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id"),
        nullable=True
    )
    po_id = Column(
        Integer,
        ForeignKey("purchase_orders.id"),
        nullable=True
    )

    quotation = relationship("Quotation")
    purchase_order = relationship("Purchase_Order")   
    project = relationship("Project", back_populates="stages")

    """" Disini buat dict kalau perlu """