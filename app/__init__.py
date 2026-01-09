from flask import Flask
from flask_migrate import Migrate
from .database import db
from .config import Config
from .routes import home_bp, user_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)

    return app
