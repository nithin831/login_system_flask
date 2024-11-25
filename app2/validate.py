import re
from flask import jsonify

def validate_user_data(data):
    """Validate user data with required fields, formats, and constraints."""

    # Validate email
    if 'email' not in data or not isinstance(data['email'], str) or not data['email']:
        return jsonify ({"message":"Email is required and should be a non-empty string."}),400
    else:
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        if not email_pattern.match(data['email']):
            return jsonify({"message":"Invalid email format.."})
    
    # Validate name: must be a non-empty string of appropriate length
    if 'name' not in data or not isinstance(data['name'], str) or not (3 <= len(data['name']) <= 50):
        return jsonify ({"message":"Name must be between 3 and 50 characters.."})

    if not data['password'] or not isinstance(data['password'], str):
        return jsonify({"message": "Password is required and must be a string."}), 400

    # Check data['password'] length
    if len(data['password']) < 8:
        return jsonify({"message": "Password must be at least 8 characters long."}), 400

    # Combined regex check for uppercase, lowercase, digit, and special character
    if not all([
        re.search(r"[A-Z]", data['password']),      # Must contain at least one uppercase letter
        re.search(r"[a-z]", data['password']),      # Must contain at least one lowercase letter
        re.search(r"[0-9]", data['password']),      # Must contain at least one digit
        re.search(r"[@$!%*?&]", data['password'])   # Must contain at least one special character
    ]):
        return jsonify({
            "message": "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (@, $, !, %, *, ?, &)."
        }), 400
    
