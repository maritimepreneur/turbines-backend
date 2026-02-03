from sqlalchemy import Column, Integer, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database import db

class Attendance(db.Model):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, autoincrement=True)

    date = Column(Date, nullable=False)
    clock_in = Column(JSONB, nullable=False)
    clock_out = Column(JSONB, nullable=False)
    checked = Column(Boolean, nullable=False)

    """ schema JSONB clock in dan clock out : timestamp, status, desc, latitude, longitude """

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=True
    )

    employee = relationship("Employee", back_populates="attendances")