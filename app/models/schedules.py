from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import db

class Schedule(db.Model):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)

    date = Column(DateTime, nullable=False)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=True
    )

    employee = relationship("Employee", back_populates="schedules")