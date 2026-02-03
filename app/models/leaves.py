from sqlalchemy import Column, Integer, String
from app.database import db

class Leave(db.Model):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, autoincrement=True)

    policy = Column(String, nullable=False)