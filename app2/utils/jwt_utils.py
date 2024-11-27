
import jwt
from datetime import datetime, timedelta
from config import Config

# from utils.redis_utils import redis_client

def generate_jwt(user_id, name, email, role, is_active, blacklist):
    """Generate a JWT token."""
    expiration = datetime.utcnow() + timedelta(seconds=Config.JWT_EXPIRATION_SECONDS)
    payload = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "role": role,
        "is_active": is_active,
        "blacklist": blacklist,
        "exp": expiration
    }
    token = jwt.encode(payload, Config.LOGIN_SECRET_KEY, algorithm="HS256")
    return token

def get_user_details_from_jwt(token):
    """
    Retrieve user details from JWT stored in Redis.
    If JWT is missing, assume it has expired or been removed.
    """
    try:
        # Decode the JWT to extract user info
        payload = jwt.decode(token, Config.LOGIN_SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        
        # # Check if the JWT exists in Redis
        # redis_key = f"jwt:{user_id}"
        # stored_token = redis_client.get(redis_key)

        # if stored_token is None:
        #     # Token not found in Redis, implying session has expired
        #     return {"error": "Session expired. Please log in again."}
        
        # if stored_token != token:
        #     # Token mismatch, likely invalid token
        #     return {"error": "Invalid session. Please log in again."}

        # If valid, return user details
        return {
            # "user_id": payload["user_id"],
            "email": payload["email"],
            "name": payload["name"],
            "role": payload["role"]
        }

    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}

def generate_verification_token(email):
    expiration_time = datetime.utcnow() + timedelta(minutes=5)  # 5 minutes expiration
    payload = {'email': email, 'exp': expiration_time}
    return jwt.encode(payload, Config.MAIL_SECRET_KEY, algorithm='HS256')

def decode_verification_token(token):
    try:
        payload = jwt.decode(token, Config.MAIL_SECRET_KEY, algorithms=['HS256'])
        return payload['email']
    except jwt.ExpiredSignatureError:
        raise Exception("Verification link has expired.")
    except jwt.InvalidTokenError as e:
        raise Exception("Invalid token.")
