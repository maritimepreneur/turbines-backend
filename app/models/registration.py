from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.models.meta.meta import Meta

class RegistrationPaymentStatus(Enum):
    PENDING = "Pending"
    PARTIAL = "Partial"
    PAID = "Paid"
    CANCELLED = "Cancelled"

class RegistrationPaymentType(Enum):
    FULL = "Full"
    CREDIT = "Credit"

class TraningCourseLevel(Enum):
    FND = "Foundation"
    SPC = "Specialization"
    EXE = "Executive"
    FNS = "Foundation and Specialization"

class Registration(db.Model, Meta):
    __tablename__ = "registration"

    id = Column(Integer, primary_key=True, autoincrement=True)
    training_course_level = Column(
        SQLEnum(TraningCourseLevel, name="training_course_level_enum"),
        nullable=False
    )
    payment_type = Column(
        SQLEnum(RegistrationPaymentType, name="registration_payment_type_enum"),
        nullable=False
    )
    payment_status = Column(
        SQLEnum(RegistrationPaymentStatus, name="registration_payment_status_enum"),
        nullable=False
    )
    payments = Column(JSONB, nullable=False)
    due_date = Column(Date, nullable=False)
    participant_code = Column(String, nullable=False)

    formdata_id = Column(
        Integer,
        ForeignKey("formdata.id"),
        nullable=True
    )

    specialization_id = Column(
        Integer,
        ForeignKey("specialization.id"),
        nullable=True
    )
    
    scholarship_id = Column(
        Integer,
        ForeignKey("scholarship.id"),
        nullable=True
    )

    formdata = relationship("FormData", back_populates="registration")
    specialization = relationship("Specialization", back_populates="registration")
    scholarship = relationship("Scholarship", back_populates="registration")    
    payments = relationship("Payment", back_populates="registration")
    
    def to_dict(self):
        return {
            "id": self.id,
            "traning_course_level": self.training_course_level.value if self.training_course_level else None,
            "payment_type": self.payment_type.value if self.payment_type else None,
            "payment_status": self.payment_status.value if self.payment_status else None,
            "payments": {
                
            },
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "participant_code": self.participant_code,
            "formdata": {

            },
            "specialization": {

            },
            "scholarship": {

            },
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }
