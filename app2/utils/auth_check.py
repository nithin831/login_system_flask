from functools import wraps
import jwt
from flask import request
from config import Config

def is_sign_in(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        header = request.headers.get("Authorization")
        if not header:
            return {"error": "Sign in is required."}
        try:
            payload = jwt.decode(header, Config.SECRET_KEY, algorithms=["HS256"])
            result = func(*args, email=payload["email"], **kwargs)
            return result
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired."}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token."}
    return decorator

def is_admin(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        header = request.headers.get("Authorization")
        if not header:
            return {"error": "Sign in is required."}
        try:
            payload = jwt.decode(header, Config.SECRET_KEY, algorithms=["HS256"])
            role = payload["role"]
            if role == "admin":
                result = func(*args, **kwargs)
                return result
            return {"message":"Permission denied"}
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired."}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token."}
    return decorator




