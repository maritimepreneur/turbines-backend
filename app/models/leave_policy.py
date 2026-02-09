from sqlalchemy import Column, Integer, String
from app.database import db
from sqlalchemy.orm import relationship

class Leave_Policy(db.Model):
    __tablename__ = "leave_policys"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    quota = Column(Integer, nullable=False)

    leave_historys = relationship("Leave_History", back_populates="leave_policy")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quota": self.quota
        }