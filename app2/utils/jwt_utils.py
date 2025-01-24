import jwt
from datetime import datetime, timedelta
from config import Config

def generate_login_jwt_token(name, email, role, is_active, blacklist, is2fa, type):
    """Generate a JWT token."""
    expiration = datetime.utcnow() + timedelta(seconds=Config.JWT_EXPIRATION_SECONDS)
    payload = {
        "name": name,
        "email": email,
        "role": role,
        "is_active": is_active,
        "blacklist": blacklist,
        "is_2fa": is2fa,
        "type": type,
        "exp": expiration
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    return token

def generate_verification_jwt_token(email, type):
    expiration_time = datetime.utcnow() + timedelta(minutes=5)  # 5 minutes expiration
    payload = {'email': email, "type": type, 'exp': expiration_time}
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def decode_jwt_token(token):
    try:
        print("reading user data")
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        print("this is payload:",payload)
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Verification link has expired.")
    except jwt.InvalidTokenError as e:
        raise Exception("Invalid token.")
