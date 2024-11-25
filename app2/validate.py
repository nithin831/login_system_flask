import re
from flask import jsonify

def validate_user_email(email):
    """Validate user email with required fields, formats, and constraints."""
    # Validate email
    if email:
        email_pattern = re.compile(r'^[^\d\W][\w\.-]+@[\w\.-]+\.\w+$')
        if not email_pattern.match(email):
            raise Exception("Invalid email format..")
            # return jsonify({"message":"Invalid email format.."}),400

def validate_user_name(name):
    """Validate user email with required fields, formats, and constraints."""    
    # Validate name: must be a non-empty string of appropriate length
    if name and not (3 <= len(name) <= 50):
        raise Exception("Name must be between 3 and 50 characters..")
        # return jsonify ({"message":"Name must be between 3 and 50 characters.."}), 400

def validate_user_password(password):
    """Validate user email with required fields, formats, and constraints."""
    # Check password length
    if password and len(password) < 8:
        raise Exception("Password must be at least 8 characters long.")
        # return jsonify({"message": "Password must be at least 8 characters long."}), 400

    # Combined regex check for uppercase, lowercase, digit, and special character
    if not all([
        re.search(r"[A-Z]", password),      # Must contain at least one uppercase letter
        re.search(r"[a-z]", password),      # Must contain at least one lowercase letter
        re.search(r"[0-9]", password),      # Must contain at least one digit
        re.search(r"[@$!%*?&]", password)   # Must contain at least one special character
    ]):
        raise Exception("Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@, $, !, %, *, ?, &).")
        # return jsonify({
        #     "message": "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@, $, !, %, *, ?, &)."
        # }), 400
    
def change_password_validate(data):
    if not data['new_password'] or not isinstance(data['new_password'], str):
        return jsonify({"message": "new_Password is required and must be a string."}), 400

    # Check data['new_password'] length
    if len(data['new_password']) < 8:
        return jsonify({"message": "new_Password must be at least 8 characters long."}), 400

    # Combined regex check for uppercase, lowercase, digit, and special character
    if not all([
        re.search(r"[A-Z]", data['new_password']),      # Must contain at least one uppercase letter
        re.search(r"[a-z]", data['new_password']),      # Must contain at least one lowercase letter
        re.search(r"[0-9]", data['new_password']),      # Must contain at least one digit
        re.search(r"[@$!%*?&]", data['new_password'])   # Must contain at least one special character
    ]):
        return jsonify({
            "message": "new_Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@, $, !, %, *, ?, &)."
        }), 400