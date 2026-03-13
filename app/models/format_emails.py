from sqlalchemy import Column, Integer, String, Text
from app.database import db

class FormatEmail(db.Model):
    __tablename__ = "format_emails"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    attachment = Column(String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "attachment": self.attachment
        }