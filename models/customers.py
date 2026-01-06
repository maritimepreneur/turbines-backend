from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Customers(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    invoice_id = db.Column(
        db.Integer,
        db.ForeignKey("invoice.id"),
        nullable=False
    )

    requirements_id = db.Column(
        db.Integer,
        db.ForeignKey("requirements.id"),
        nullable=False
    )

    partners_id = db.Column(
        db.Integer,
        db.ForeignKey("partners.id"),
        nullable=False
    )