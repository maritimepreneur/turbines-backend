from database import db

class Requirements(db.Model):
    __tablename__ = "requirements"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    project_location = db.Column(db.String(50), nullable=False)
    project_type = db.Column(db.String(50), nullable=False)
    project_duration = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    payment_type = db.Column(db.String(50), nullable=False)