from functools import wraps
import jwt
from flask import request
from config import Config


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization")
        if not header:
            return {"error": "Sign in is required."}
        try:
            payload = jwt.decode(header, Config.SECRET_KEY, algorithms=["HS256"])
            role = payload["role"]
            if role == "admin":
                result = fn(*args, **kwargs)
                return result
            return {"message":"Permission denied admin only can access"}
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired."}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token."}
    return wrapper