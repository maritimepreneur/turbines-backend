from sqlalchemy import Column, Integer, Date, DateTime, Boolean, ForeignKey
from app.database import db
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Leave_History(db.Model):
    __tablename__ = "leave_historys"

    id = Column(Integer, primary_key=True, autoincrement=True)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approval = Column(Boolean, nullable=False)

    leave_policy_id = Column(
        Integer,
        ForeignKey("leave_policys.id"),
        nullable=True
    )

    leave_policy = relationship("Leave_Policy", back_populates="leave_historys")

    def to_dict(self):
        return {
            "id": self.id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "approval": self.approval,
            "leave_policy_id": self.leave_policy_id
        }