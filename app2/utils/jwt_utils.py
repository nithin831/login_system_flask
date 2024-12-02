
import jwt
from datetime import datetime, timedelta
from config import Config

def generate_login_jwt_token(name, email, role, is_active, blacklist, is2fa):
    """Generate a JWT token."""
    expiration = datetime.utcnow() + timedelta(seconds=Config.JWT_EXPIRATION_SECONDS)
    payload = {
        "name": name,
        "email": email,
        "role": role,
        "is_active": is_active,
        "blacklist": blacklist,
        "is_2fa": is2fa,
        "exp": expiration
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    return token

def generate_verification_jwt_token(email):
    expiration_time = datetime.utcnow() + timedelta(minutes=5)  # 5 minutes expiration
    payload = {'email': email, 'exp': expiration_time}
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def generate_2fa_verification_jwt_token(email, is_2fa):
    expiration_time = datetime.utcnow() + timedelta(minutes=5)  # 5 minutes expiration
    payload = {'email': email, 'is_2fa':is_2fa, 'exp': expiration_time}
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Verification link has expired.")
    except jwt.InvalidTokenError as e:
        raise Exception("Invalid token.")
