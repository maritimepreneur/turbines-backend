from flask_restx import fields, Model
from app.schemas.base_schema import BaseSchema

class AuthSchema(BaseSchema):
    
    @classmethod
    def register_schema(cls, namespace: Model):
  
        return namespace.model("RegisterRequest", {
            "username": fields.String(required=True, description="Username"),
            "email": fields.String(required=True, description="Email address"),
            "password": fields.String(required=True, description="Password"),
            "confirm_password": fields.String(required=True, description="Confirm password"),
            "role": fields.String(required=False, default="USER", description="User role (ADMIN, BIZDEV, FINANCE, OPERATION, USER)")
        })
    
    @classmethod
    def login_schema(cls, namespace: Model):
        """ Schema for user login """
        return namespace.model("LoginRequest", {
            "identifier": fields.String(required=True, example="testuser", description="Username or Email"),
            "password": fields.String(required=True, example="password123", description="Password")
        })
    
    @classmethod
    def user_response_schema(cls, namespace: Model):

        user_data = namespace.model("UserData", {
            "id": fields.Integer,
            "username": fields.String,
            "email": fields.String,
            "role": fields.String,
            "created_at": fields.String
        })
        
        return namespace.model("UserResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(user_data)
        })
    
    @classmethod
    def token_response_schema(cls, namespace: Model):
        """ Schema for token response """
        user_data = namespace.model("TokenUserData", {
            "id": fields.Integer,
            "username": fields.String,
            "email": fields.String,
            "role": fields.String,
            "created_at": fields.String
        })
        
        token_data = namespace.model("TokenData", {
            "access_token": fields.String,
            "refresh_token": fields.String,
            "user": fields.Nested(user_data)
        })
        
        return namespace.model("TokenResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(token_data)
        })
    
    @classmethod
    def validate_response_schema(cls, namespace: Model):
        """ Schema for token validation response """
        validate_data = namespace.model("ValidateData", {
            "user_id": fields.Integer,
            "username": fields.String,
            "role": fields.String
        })
        
        return namespace.model("ValidateResponse", {
            **BaseSchema.get_schema(namespace),
            "data": fields.Nested(validate_data)
        })