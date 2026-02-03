from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import db

class CV_Tracker(db.Model):
    __tablename__ = "cv_trackers"

    id = Column(Integer, primary_key=True, autoincrement=True)

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=True
    )
    requirement_id = Column(
        Integer,
        ForeignKey("requirements.id"),
        nullable=False
    )

    candidate = relationship("Candidate", back_populates="cv_trackers")
    requirement = relationship("Requirement", back_populates="cv_trackers")