from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restx import Api
from .database import db
from .config import Config
from .routes import home_bp, user_bp
from .routes.auth_routes import auth_bp
from .routes.contact_routes import contact_ns

migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            'success': False,
            'message': 'Token has expired'
        }, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            'success': False,
            'message': 'Invalid token'
        }, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            'success': False,
            'message': 'Authorization token is missing'
        }, 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {
            'success': False,
            'message': 'Token has been revoked'
        }, 401


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"Invalid token error: {error}")  # Debug log
        return {
            'success': False,
            'message': f'Invalid token: {error}'
    }, 401

    api = Api(app)
    api.add_namespace(contact_ns, path="/contacts")

    return app