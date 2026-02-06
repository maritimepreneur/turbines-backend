from sqlalchemy import Column, String, Integer, Time, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import db
from sqlalchemy.dialects.postgresql import JSONB

class Schedule(db.Model):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    date = Column(DateTime, nullable=False)
    tagged_ids = Column(JSONB, nullable=False, default=list, server_default="[]")

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=True
    )

    employee = relationship("Employee", back_populates="schedules")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "date": self.date.isoformat() if self.date else None,
            "tagged_ids": self.tagged_ids,
            "employee_id": self.employee_id
        }