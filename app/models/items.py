from app.database import db
from enum import Enum
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.models.meta.meta import Meta

class ItemType(Enum):
    SERVICE = "Service"
    GOODS = "Goods"

class AmountType(Enum):
    PCS = "Pcs"
    KG = "Kg"
    ITEM = "Item"
    LITER = "Liter"
    METER = "Meter"
    BOX = "Box"
    PACK = "Pack"
    HOUR = "Hour"
    DAY = "Day"
    SESSION = "Session"

class Item(db.Model, Meta):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cost = Column(Numeric(14, 2), nullable=False) #Harga Awal
    amount = Column(Numeric(14, 2), nullable=False) #Jumlah Barang
    billed_amount = Column(Numeric(14, 2), nullable=False) #Harga+Tax/Markup
    type = Column(
        SQLEnum(ItemType, name="item_type_enum"),
        nullable=False
    )
    amount_type = Column(
        SQLEnum(AmountType, name="item_amount_type_enum"),
        nullable=True)
    code = Column(String, nullable=False)
    attachments = Column(JSONB, nullable=False, default=list, server_default="[]")

    __table_args__ = (
        UniqueConstraint("code", name="uq_item_code"),
    )

    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id"),
        nullable=True
    )

    quotation = relationship("Quotation", back_populates="items")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cost": float(self.cost),
            "amount": float(self.amount),
            "billed_amount": float(self.billed_amount),
            "type": self.type.value if self.type else None,
            "amount_type": self.amount_type,
            "code": self.code,
            "attachments": self.attachments,
            "meta": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "created_by": self.created_by,
                "updated_by": self.updated_by
            }
        }