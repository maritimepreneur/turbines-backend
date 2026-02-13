from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt


from flask import jsonify

def response(code: int = None, message: str = None, data: dict = None):
    _response = {"message": message}
    if code is not None:
        _response.update({"code": code})
    if data is not None:
        _response.update({"data": data})
    return _response, code


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            user_role = claims.get("role")
            if user_role not in allowed_roles:
                return {
                    "code": 403,
                    "message": "Forbidden: insufficient role"
                }, 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator