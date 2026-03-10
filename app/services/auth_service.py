from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from typing import Optional, Dict, Any

from app.models.users import User, UserRole
from app.services.base_service import BaseService
from app.utils import response

class AuthService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def register_user(self, data: Dict[str, Any]):

        try:
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            role_name = data.get('role', 'USER').upper()

            if not all([username, email, password, confirm_password]):
                return response(400, "All fields (Username, Email, Password, Confirm Password) are required")

            if password != confirm_password:
                return response(400, "Password and Confirm Password do not match")

            existing_user = self.db.query(User).filter(
                (User.email == email) | (User.username == username)
            ).first()
            
            if existing_user:
                return response(409, "Username or Email already registered")

            try:
                role_enum = UserRole[role_name]
            except KeyError:
                return response(400, f"Role {role_name} is not valid")

            new_user = User(
                username=username,
                email=email,
                role=role_enum
            )
            new_user.set_password(password)

            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            return response(201, "User registered successfully", self._serialize_user(new_user))

        except IntegrityError:
            self.db.rollback()
            return response(400, "Data integrity error (Possible duplicate username/email)")
        except Exception as e:
            self.db.rollback()
            return response(500, str(e))
    
    def login_user(self, data: Dict[str, Any]):

        try:
            identifier = data.get('identifier')
            password = data.get('password')
            
            if not identifier or not password:
                return response(400, "Identifier and password are required")
            
            user = self._authenticate_user(identifier, password)
            
            if not user:
                return response(401, "Invalid credentials")
            
            additional_claims = {
                "role": user.role.value if hasattr(user.role, "value") else user.role,
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
            
            return response(200, "Login successful", {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": self._serialize_user(user)
            })
            
        except Exception as e:
            return response(500, str(e))
        
    def update_password(self, user_id: int, data: Dict[str, Any]):

        try:
            current_password = data.get("current_password")
            new_password = data.get("new_password")
            confirm_password = data.get("confirm_password")

            if not all([current_password, new_password, confirm_password]):
                return response(400, "All fields are required")

            if new_password != confirm_password:
                return response(400, "New password and confirm password do not match")
            
            if len(new_password) < 8:
                return response(400, "New password must be at least 8 characters long")

            user = self.db.query(User).get(user_id)

            if not user:
                return response(404, "User not found")

            if not user.check_password(current_password):
                return response(401, "Current password is incorrect")
            
            user.set_password(new_password)

            self.db.commit()

            return response(200, "Password updated successfully")

        except Exception as e:
            self.db.rollback()
            return response(500, str(e))
    
    def refresh_token(self, user_id: str, claims: Dict[str, Any]):
        """ Refresh access token """
        try:
            additional_claims = {
                "role": claims.get("role"),
                "username": claims.get("username")
            }
            
            access_token = create_access_token(
                identity=user_id,
                additional_claims=additional_claims,
                expires_delta=timedelta(hours=1)
            )
            
            return response(200, "Token refreshed successfully", {
                "access_token": access_token
            })
            
        except Exception as e:
            return response(500, str(e))
    
    def validate_token(self, user_id: int, claims: Dict[str, Any]):
        """ Validate current token """
        return response(200, "Token is valid", {
            "user_id": user_id,
            "username": claims.get("username"),
            "role": claims.get("role")
        })
    
    def _authenticate_user(self, identifier: str, password: str) -> Optional[User]:
        """ Authenticate user by username/email and password """
        try:
            user = self.db.query(User).filter(
                (User.username == identifier) | (User.email == identifier)
            ).first()
            
            if not user:
                return None
            
            if not user.check_password(password):
                return None
            
            return user
            
        except SQLAlchemyError as e:
            print(f"Database error during authentication: {str(e)}")
            return None
    
    def _serialize_user(self, user: User) -> Dict[str, Any]:
        """ Serialize user object to dictionary """
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value if hasattr(user.role, "value") else user.role,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }