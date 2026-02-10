from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restx import Api
from .database import db
from .config import Config
from flask_cors import CORS

migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},  
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            'success': False,
            'message': 'Token has expired'
        }, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"Invalid token error: {error}")
        return {
            'success': False,
            'message': f'Invalid token: {error}'
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

    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "JWT Authorization header using the Bearer scheme. Example: \"Bearer {token}\""
        }
    }
    
    api = Api(
        app,
        version='1.0',
        title='Turbinz API',
        description='API Documentation for Turbinz Application',
        doc='/api/docs',
        authorizations=authorizations,
        security='Bearer Auth'
    )

    # Import namespaces
    from .routes import auth_ns, contact_ns, partner_ns, lead_ns, employee_ns, attendance_ns, vendor_ns, quotation_ns
    
    # Register namespaces dengan prefix /api
    api.add_namespace(auth_ns, path="/api/auth")
    api.add_namespace(contact_ns, path="/api/contacts")
    api.add_namespace(partner_ns, path="/api/partners")
    api.add_namespace(lead_ns, path="/api/leads")
    api.add_namespace(vendor_ns, path="/api/vendors")
    api.add_namespace(employee_ns, path="/api/employees")
    api.add_namespace(attendance_ns, path="/api/attendances")
    api.add_namespace(quotation_ns, path="/api/quotations")


    return app