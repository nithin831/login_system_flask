import re
import pyotp
from user import fetch_secret_key
from flask import jsonify

def validate_user_email(email):
    """Validate user email with required fields, formats, and constraints."""
    # Validate email
    if email:
        email_pattern = re.compile(r'^[^\d\W][\w\.-]+@[\w\.-]+\.\w+$')
        if not email_pattern.match(email):
            return False, "Invalid email format.."
    return True, "Proceed."

def validate_user_name(name):
    """Validate user email with required fields, formats, and constraints."""    
    # Validate name: must be a non-empty string of appropriate length
    if name and not (3 <= len(name) <= 50):
        return False, "Name must be between 3 and 50 characters.."
    return True, "Proceed."

def validate_user_password(password):
    """Validate user email with required fields, formats, and constraints."""
    # Check password length
    if password and len(password) < 8:
        return False, "Password must be at least 8 characters long."
    # Combined regex check for uppercase, lowercase, digit, and special character
    if not all([
        re.search(r"[A-Z]", password),      # Must contain at least one uppercase letter
        re.search(r"[a-z]", password),      # Must contain at least one lowercase letter
        re.search(r"[0-9]", password),      # Must contain at least one digit
        re.search(r"[@$!%*?&]", password)   # Must contain at least one special character
    ]):
        return False, "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@, $, !, %, *, ?, &)."
    return True, "Proceed."

def verify_totp(email, totp_token):
    secret = fetch_secret_key(email)
    totp = pyotp.TOTP(secret[0])
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
    # Validate per_page
    try:
        per_page = int(per_page)
        print(per_page)
        if per_page < 1 or per_page > 10:
            return False, "Per page must be between 1 and 10."
    except Exception:
        return False, "Per page must be an integer."
    return True, None
