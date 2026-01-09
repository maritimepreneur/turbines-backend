from app.models.users import User
from app.database import db
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, Dict, Any

class AuthService:
    """Service layer for authentication operations"""
    
    @staticmethod
    def authenticate_user(identifier: str, password: str) -> Optional[User]:
        """
        Authenticate user by username/email and password
        
        Args:
            identifier: Username or email
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        try:
            # Try to find user by username or email
            user = User.query.filter(
                (User.username == identifier) | (User.email == identifier)
            ).first()
            
            if not user:
                return None
            
            # Check password
            if not user.check_password(password):
                return None
            
            return user
            
        except SQLAlchemyError as e:
            # Log error in production
            print(f"Database error during authentication: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object if found, None otherwise
        """
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            print(f"Database error getting user: {str(e)}")
            return None
    
    @staticmethod
    def serialize_user(user: User) -> Dict[str, Any]:
        """
        Serialize user object to dictionary
        
        Args:
            user: User object
            
        Returns:
            Dictionary with user data (excluding sensitive info)
        """
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "customer_id": user.customer_id,
            "partner_id": user.partner_id,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }