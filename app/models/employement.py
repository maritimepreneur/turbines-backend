from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import db
from app.models.meta.meta import Meta

class JobType(Enum):
    INTERN = "Internship"
    FULLTIME = "Full-time"
    PARTTIME = "Part-time"
    EXECUTIVE = "Executive"

class Empolyement(db.Model, Meta):
    __tablename__ = "employements"

    id = Column(Integer, primary_key=True, autoincrement=True)

    effective_start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    departement = Column(String, nullable=False)
    division = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    job_position = Column(
        SQLEnum(JobType, name="employement_job_type"),
        nullable=False
    )
    employee_type = Column(Boolean, nullable=False)
    client = Column(Boolean, nullable=False)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=True,
        unique=True
    )

    employee = relationship("Employee", back_populates="employement")


    def to_dict(self):
        return {
            "id": self.id,
            "effective_start_date": self.effective_start_date,
            "end_date": self.end_date,
            "departement": self.departement,
            "division": self.division,
            "job_title": self.job_title,
            "job_position": self.job_position.value if self.job_position else None,
            "employee_type": self.employee_type,
            "client": self.client,
            "employee_id": self.employee_id,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }