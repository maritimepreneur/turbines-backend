from sqlalchemy import Column, DateTime, Integer
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

class Meta:
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Jakarta")),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Jakarta")),
        onupdate=lambda: datetime.now(ZoneInfo("Asia/Jakarta")),
        nullable=False
    )
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    @property
    def meta(self):
        return {
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
        }