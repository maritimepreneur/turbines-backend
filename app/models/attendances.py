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

    def to_dict(self):
        """Helper to convert SQLAlchemy object to Dictionary"""
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "clock_in": self.clock_in if self.clock_in else {},
            "clock_out": self.clock_out if self.clock_out else {},
            "checked": self.checked,
            "employee_id": self.employee_id,
            "employee_name": self.employee.full_name if self.employee else None  # ← pastiin ini ada
        }