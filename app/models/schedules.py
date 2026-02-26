from sqlalchemy import Column, String, Integer, Time, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import db
from sqlalchemy.dialects.postgresql import JSONB
from app.models.meta.meta import Meta

class Schedule(db.Model, Meta):
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
            "date": str(self.date) if self.date else None,
            "tagged_ids": self.tagged_ids if self.tagged_ids else [],
            "employee_id": self.employee_id,
            "employee": {
                "id": self.employee.id,
                "full_name": self.employee.full_name,
                "employee_code": self.employee.employee_code,
                "email": self.employee.email
            } if self.employee else None,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }