from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.database import db
from app.services.auth_service import AuthService
from app.schemas.auth_schema import AuthSchema

auth_ns = Namespace("auth", description="Authentication Management")
auth_svc = AuthService(db.session)

register_schema = AuthSchema.register_schema(auth_ns)
login_schema = AuthSchema.login_schema(auth_ns)
token_response_schema = AuthSchema.token_response_schema(auth_ns)
user_response_schema = AuthSchema.user_response_schema(auth_ns)
validate_response_schema = AuthSchema.validate_response_schema(auth_ns)
update_password_schema = AuthSchema.update_password_schema(auth_ns)

@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_schema)
    @auth_ns.marshal_with(user_response_schema)
    def post(self):
        """ Register a new user """
        return auth_svc.register_user(auth_ns.payload)

@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_schema)
    @auth_ns.marshal_with(token_response_schema)
    def post(self):
        """ Login user """
        return auth_svc.login_user(auth_ns.payload)

@auth_ns.route("/refresh")
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    @auth_ns.doc(security="Bearer Auth")
    @auth_ns.marshal_with(token_response_schema)
    def post(self):
        """ Refresh access token """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        return auth_svc.refresh_token(current_user_id, claims)

@auth_ns.route("/validate")
class ValidateToken(Resource):
    @jwt_required()
    @auth_ns.doc(security="Bearer Auth")
    @auth_ns.marshal_with(validate_response_schema)
    def get(self):
        """ Validate current token """
        user_id = int(get_jwt_identity())
        claims = get_jwt()
        return auth_svc.validate_token(user_id, claims)
    
@auth_ns.route("/update-password")
class UpdatePassword(Resource):

    @jwt_required()
    @auth_ns.doc(security="Bearer Auth")
    @auth_ns.expect(update_password_schema)
    def post(self):
        """ Update user password """
        user_id = int(get_jwt_identity())
        return auth_svc.update_password(user_id, auth_ns.payload)