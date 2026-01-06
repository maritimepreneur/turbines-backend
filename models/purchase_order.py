from database import db

class Purchase_Order(db.Model):
    __tablename__ = "purchase_order"

    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.Integer, nullable=False)
    attachment_name = db.Column(db.String(255), nullable=False)
    attachment_path = db.Column(db.String(255), nullable=False)
    attachment_type = db.Column(db.String(50))
    total_amount = db.Column(db.Numeric(14, 2), nullable=False)

    partners_id = db.Column(
        db.Integer,
        db.ForeignKey("partners.id"),
        nullable=False
    )

    requirements_id = db.Column(
        db.Integer,
        db.ForeignKey("requirements.id"),
        nullable=False
    )