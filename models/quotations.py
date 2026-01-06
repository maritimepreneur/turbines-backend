from database import db

class Quotations(db.Model):
    __tablename__ = "quotations"

    id = db.Column(db.Integer, primary_key=True)
    document_number = db.Column(db.Integer, nullable=False)
    document_name = db.Column(db.String(100), nullable=False)
    document_content = db.Column(db.Text)
    total_amount = db.Column(db.Numeric(14, 2), nullable=False)

    requirements_id = db.Column(
        db.Integer,
        db.ForeignKey("requirements.id"),
        nullable=False
    )