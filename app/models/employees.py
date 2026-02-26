from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Date, UniqueConstraint, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import db
from app.models.meta.meta import Meta

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

class Employee(db.Model, Meta):
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
        UniqueConstraint("employee_code", name="uq_emplyee_code"),
    )

    user = relationship("User", back_populates="employee")
    schedules = relationship("Schedule", back_populates="employee", cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")

    def to_dict(self):
        """Helper untuk mengubah Object Employee ke Dictionary agar JSON Serializable"""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "nickname": self.nickname,
            "residence_address": self.residence_address,
            "permanent_address": self.permanent_address,
            "birth_place": self.birth_place,
            "birth_date": str(self.birth_date) if self.birth_date else None,
            "religion": self.religion.value if self.religion else None,
            "blood_type": self.blood_type.value if self.blood_type else None,
            "nationality": self.nationality,
            "marital_status": self.marital_status.value if self.marital_status else None,
            "ktp": self.ktp,
            "driving_license": self.driving_license,
            "npwp": self.npwp,
            "phone": self.phone,
            "whatsapp": self.whatsapp,
            "email": self.email,
            "handphone": self.handphone,
            "employee_code": self.employee_code,
            "img_url": self.img_url,
            "signature_img_url": self.signature_img_url,
            "signature_scale": self.signature_scale,
            "user_id": self.user_id,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }