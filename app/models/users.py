from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserRole(Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    BIZDEV = "BIZDEV"
    FINANCE = "FINANCE"
    OPERATION = "OPERATION"

class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(
        SQLEnum(UserRole, name="user_role_enum"),
        default=UserRole.USER,
        nullable=False
    )
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("username", name="uq_user_username"),
        UniqueConstraint("email", name="uq_user_email"),
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=True
    )
    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )

    customer = relationship("Customer", back_populates="users")
    partner = relationship("Partner", back_populates="users")

    def set_password(self, password):
        """ Hash and store password """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ Check if password equals to stored hash """
        return check_password_hash(self.password_hash, password)
    
    """ Disini buat dict kalau perlu """