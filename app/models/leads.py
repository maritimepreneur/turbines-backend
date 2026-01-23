from app.database import db
from sqlalchemy import Column, Integer, String, Text, DATE, ForeignKey
from sqlalchemy.orm import relationship

class Lead(db.Model):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    period = Column(DATE, nullable=False)
    description = Column(Text, nullable=False)

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id"),
        nullable=True
    )
    partner_id = Column(
        Integer,
        ForeignKey("partners.id"),
        nullable=True
    )

    # Relationships
    contact = relationship("Contact", back_populates="leads")
    partner = relationship("Partner", back_populates="leads")
    projects = relationship("Project", back_populates="lead")

    def to_dict(self):
        """ Helper to convert SQLAlchemy object to Dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "period": self.period.isoformat() if self.period else None,
            "description": self.description,
            "contact_id": self.contact_id,
            "partner_id": self.partner_id,
            # Flatten nested data for display if needed
            "contact_name": self.contact.name if self.contact else None,
            "company": self.contact.company if self.contact else None, # Company comes from Contact
            "partner_name": self.partner.name if self.partner else None
        }