from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.meta.meta import Meta

class SelectionStatus(Enum):
    ELIGIBLE = "Eligible"
    INELIGIBLE = "Ineligible"

class FormData(db.Model, Meta):
    __tablename__ = "formdata"

    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_number = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    nama_lengkap = Column(String, nullable=False)
    nomor_whatsapp = Column(String, nullable=False)
    tempat_lahir = Column(String, nullable=False)
    jenis_kelamin = Column(String, nullable=False)
    alamat_ktp = Column(String, nullable=False)
    domisili = Column(String, nullable=False)
    pendaftaran = Column(String, nullable=False)
    prodi = Column(String, nullable=False)
    status_pendidikan = Column(String, nullable=False)
    instansi_pendidikan_akhir = Column(String, nullable=False)
    link_cv = Column(String, nullable=False)
    is_email_sent = Column(Boolean, nullable=True)
    interview_datetime = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, nullable=False)
    selection_status = Column(
        SQLEnum(SelectionStatus, name="selection_status_enum"),
        nullable=True
    )

    registration = relationship("Registration", back_populates="formdata")

    def to_dict(self):
        return {
            "id": self.id,
            "batch_number": self.batch_number,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "nama_lengkap": self.nama_lengkap,
            "nomor_whatsapp": self.nomor_whatsapp,
            "tempat_lahir": self.tempat_lahir,
            "jenis_kelamin": self.jenis_kelamin,
            "alamat_ktp": self.alamat_ktp,
            "domisili": self.domisili,
            "pendaftaran": self.pendaftaran,
            "prodi": self.prodi,
            "status_pendidikan": self.status_pendidikan,
            "instansi_pendidikan_akhir": self.instansi_pendidikan_akhir,
            "link_cv": self.link_cv,
            "is_email_sent": self.is_email_sent,
            "interview_datetime": self.interview_datetime.isoformat() if self.interview_datetime else None,
            "status": self.status,
            "selection_status": self.selection_status.value if self.selection_status else None,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }