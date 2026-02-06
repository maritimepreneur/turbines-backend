from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import db
from sqlalchemy.dialects.postgresql import JSONB

class Candidate(db.Model):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    red_flag = Column(Boolean, nullable=False)
    reason = Column(String, nullable=False)
    cv_source = Column(JSONB, nullable=False, server_default="{}")
    referrer_name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    cv_trackers = relationship("CV_Tracker", back_populates="candidate")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "red_flag": self.red_flag,
            "reason": self.reason,
            "cv_source": self.cv_source,
            "referrer_name": self.referrer_name,
            "description": self.description,
        }