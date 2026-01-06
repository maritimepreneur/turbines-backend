from database import db

class Invoice(db.Model):
    __tablename__ = "invoice"

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.Integer, nullable=False)
    created = db.Column(db.Date, nullable=False)
    period = db.Column(db.String(50), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    billed_amount = db.Column(db.Numeric(14, 2), nullable=False)
    total_amount = db.Column(db.Numeric(14, 2), nullable=False)
    notes = db.Column(db.Text)

    partners_id = db.Column(
        db.Integer,
        db.ForeignKey("partners.id"),
        nullable=False
    )

    purchase_order_id = db.Column(
        db.Integer,
        db.ForeignKey("purchase_order.id"),
        nullable=False
    )

    requirements_id = db.Column(
        db.Integer,
        db.ForeignKey("requirements.id"),
        nullable=False
    )