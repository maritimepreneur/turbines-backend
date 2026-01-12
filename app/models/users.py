from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
<<<<<<< HEAD:models/users.py
from sqlalchemy.sql import func
from database import db
=======
from app.database import db
>>>>>>> b555cf52f10e667dc5684d4b41e152acd85ba334:app/models/users.py
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

    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )

    partner = relationship("Partner", back_populates="users")

    def set_password(self, password):
<<<<<<< HEAD:models/users.py
        """ Hash and store password """
=======
>>>>>>> b555cf52f10e667dc5684d4b41e152acd85ba334:app/models/users.py
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    