from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import db

class Requirement(db.Model):
    __tablename__ = "requirements"

    id = Column (Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)

    cv_trackers = relationship("CV_Tracker", back_populates="requirement")