from app.models.users import User, UserRole
from app.database import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Optional, Dict, Any

class AuthService:
    
    @staticmethod
    def authenticate_user(identifier: str, password: str) -> Optional[User]:
        try:
            user = User.query.filter(
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
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            print(f"Database error getting user: {str(e)}")
            return None

    @staticmethod
    def register_user(data: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
        try:
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            role_name = data.get('role', 'USER').upper()

            if not all([username, email, password, confirm_password]):
                return {"success": False, "message": "Semua field (Username, Email, Password, Confirm Password) harus diisi"}, 400

            if password != confirm_password:
                return {"success": False, "message": "Password dan Konfirmasi Password tidak cocok"}, 400

            existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
            if existing_user:
                return {"success": False, "message": "Username atau Email sudah terdaftar"}, 409

            try:
                role_enum = UserRole[role_name]
            except KeyError:
                return {"success": False, "message": f"Role {role_name} tidak valid"}, 400

            new_user = User(
                username=username,
                email=email,
                role=role_enum
            )
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            return {
                "success": True,
                "message": "User berhasil didaftarkan",
                "data": AuthService.serialize_user(new_user)
            }, 201

        except IntegrityError:
            db.session.rollback()
            return {"success": False, "message": "Kesalahan integritas data (Mungkin username/email duplikat)"}, 400
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": str(e)}, 500

    @staticmethod
    def serialize_user(user: User) -> Dict[str, Any]:
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "customer_id": user.customer_id,
            "partner_id": user.partner_id,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }