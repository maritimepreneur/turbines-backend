from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from datetime import timedelta
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({
            "success": False,
            "message": "Content-Type must be application/json"
        }), 400
    
    data = request.get_json()
    
    identifier = data.get('identifier')
    password = data.get('password')
    
    if not identifier or not password:
        return jsonify({
            "success": False,
            "message": "identifier and password are required"
        }), 400
    
    user = AuthService.authenticate_user(identifier, password)
    
    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid credentials"
        }), 401
    
    additional_claims = {
        "role": user.role.value,
        "username": user.username
    }
    
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=1)
    )
    
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims=additional_claims,
        expires_delta=timedelta(days=30)
    )
    
    return jsonify({
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": AuthService.serialize_user(user)
        }
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    additional_claims = {
        "role": claims.get("role"),
        "username": claims.get("username")
    }
    
    access_token = create_access_token(
        identity=current_user_id,
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=1)
    )
    
    return jsonify({
        "success": True,
        "message": "Token refreshed successfully",
        "data": {
            "access_token": access_token
        }
    }), 200


@auth_bp.route('/validate', methods=['GET'])
@jwt_required()
def validate_token():
    user_id = int(get_jwt_identity())
    claims = get_jwt()

    return jsonify({
        "success": True,
        "message": "Token is valid",
        "data": {
            "user_id": user_id,
            "username": claims.get("username"),
            "role": claims.get("role")
        }
    }), 200

