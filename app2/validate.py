import re
import pyotp
from user import fetch_secret_key
from flask import request, jsonify
from functools import wraps

def validate_user_email(email):
    if email:
        email_pattern = re.compile(r'^[^\d\W][\w\.-]+@[\w\.-]+\.\w+$')
        if not email_pattern.match(email):
            return False, "Invalid email format.."
    return True, "Proceed."

def validate_user_name(name):
    if name and not (3 <= len(name) <= 50):
        return False, "Name must be between 3 and 50 characters.."
    return True, "Proceed."

def validate_user_password(password):
    if password and len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not all([
        re.search(r"[A-Z]", password),
        re.search(r"[a-z]", password),
        re.search(r"[0-9]", password),
        re.search(r"[@$!%*?&]", password)
    ]):
        return False, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@, $, !, %, *, ?, &)."
    return True, "Proceed."

def verify_totp(email, totp_token):
    secret = fetch_secret_key(email)
    totp = pyotp.TOTP(secret["secret_key"])
    if not totp.verify(totp_token):
        return False
    return True

def validate_pagination(page, per_page):
    try:
        page = int(page)
        print(page)
        if page < 1:
            return False, "Page number must be a positive integer."
    except Exception:
        return False, "Page number must be an integer."
    try:
        per_page = int(per_page)
        print(per_page)
        if per_page < 1 or per_page > 10:
            return False, "Per page must be between 1 and 10."
    except Exception:
        return False, "Per page must be an integer."
    return True, None

def validate_request(required_fields):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            print("this validate data:",data)
            if not data:
                return jsonify({"error": "Invalid payload"}), 400
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400
            return func(*args, **kwargs)
        return wrapper
    return decorator