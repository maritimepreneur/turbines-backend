from database import db

class Partners(db.Model):
    __tablename__= "partners"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    requirements_id = db.Column(
        db.Integer,
        db.ForeignKey("requirements.id"),
        nullable=False
    )