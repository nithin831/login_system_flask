import bcrypt
from flask import jsonify, Blueprint, request
from user import *
from validate import *
from utils.jwt_utils import generate_jwt

sign_in_bp = Blueprint('sign_in_bp', __name__)
@sign_in_bp.post('/sign-in')
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400
    try:
        response, message = validate_user_email(email)
        if not response:
            return jsonify({"message": message})
        user = sign_in(email)
        if not user:
            return jsonify({"error": "User not found."}), 400
        user_id, stored_password, stored_role, is_active, name, blacklist, is_2fa = user
        # Check if user is active
        if blacklist:
            return jsonify({"error": "User is Blacklisted. Please contact support."}), 400
        if not is_active:
            return jsonify({"error": "User not found."}), 400
        # Validate the password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.tobytes()):
            if is_2fa:
                if request.args.get("otp"):
                    totp_token = request.args.get("otp")
                    verification = verify_totp(email, totp_token)
                    if not verification:
                        return jsonify({"error": "Invalid otp"}), 400
                    return {"message": "Valid OTP. Login sucessful.", "token": generate_jwt(user_id, name, email, stored_role, is_active, blacklist)}
                return {"message": "Enter the OTP from the Authenticator App."}
            return {"message": "Login sucessful.", "token":generate_jwt(user_id, name, email, stored_role, is_active, blacklist)}
        else:
            return jsonify({"error": "User not found or incorrect credentials."}), 400
    except Exception as e:
        # raise e
        return jsonify({"error": str(e)}), 400