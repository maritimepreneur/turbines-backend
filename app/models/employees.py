from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Date, UniqueConstraint, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import db

class Religion(Enum):
    ISLAM = "ISLAM"
    CHRISTIANITY = "CHRISTIANITY"
    HINDUISM = "HINDUISM"
    BUDDHISM = "BUDDHISM"
    CONFUCIANISM = "CONFUCIANISM"
    OTHER = "OTHER"

class BloodType(Enum):
    APLUS = "A+"
    AMIN = "A-"
    BPLUS = "B+"
    BMIN = "B-"
    OPLUS = "O+"
    OMIN = "O-"
    ABPLUS = "AB+"
    ABMIN = "AB-"

class MaritalStatus(Enum):
    SINGLE = "SINGLE"
    MARRIED = "MARRIED"
    WIDOWED = "WIDOWED"
    DIVORCED = "DIVORCED"
    SEPARATED = "SEPARATED"

class Employee(db.Model):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)

    full_name = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    residence_address = Column(String, nullable=False)
    permanent_address = Column(String, nullable=False)
    birth_place = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    religion = Column(
        SQLEnum(Religion, name="employee_religion_enum"),
        default=Religion.OTHER,
        nullable=False
    )
    blood_type = Column(
        SQLEnum(BloodType, name="employee_blood_enum"),
        nullable=False
    )
    nationality = Column(String, nullable=False)
    marital_status = Column(
        SQLEnum(MaritalStatus, name="employee_marital_enum"),
        default=MaritalStatus.SINGLE,
        nullable=False
    )
    ktp = Column(String, nullable=False)
    driving_license = Column(String, nullable=False)
    npwp = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    whatsapp = Column(String, nullable=False)
    email = Column(String, nullable=False)
    handphone = Column(String, nullable=False)
    employee_code = Column(String, nullable=False)
    img_url = Column(String, nullable=False)
    signature_img_url = Column(String, nullable=False)
    signature_scale = Column(Float, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        unique=True
    )

    __table_args__ = (
        UniqueConstraint("nickname", name="uq_employee_nickname"),
    )

    user = relationship("User", back_populates="employee")
    schedules = relationship("Schedule", back_populates="employee")
    attendances = relationship("Attendance", back_populates="employee")