import bcrypt
from flask import jsonify, Blueprint, request
from user import *
from validate import *
from utils.jwt_utils import generate_login_jwt_token, decode_jwt_token, generate_2fa_verification_jwt_token

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
        stored_password, stored_role, is_active, name, blacklist, is_2fa = user
        # Check if user is active
        if blacklist:
            return jsonify({"error": "User is Blacklisted. Please contact support."}), 400
        if not is_active:
            return jsonify({"error": "User not found."}), 400
        # Validate the password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.tobytes()):
            if is_2fa:
                jwt_token = generate_2fa_verification_jwt_token(email, is_2fa)
                return {"message": "Enter the OTP from the Authenticator App.", "jwt_token_for_2fa_to_verify": jwt_token}
            return {"message": "Login sucessful.", "token":generate_login_jwt_token(name, email, stored_role, is_active, blacklist)}
        else:
            return jsonify({"error": "User not found or incorrect credentials."}), 400
    except Exception as e:
        # raise e
        return jsonify({"error": str(e)}), 400

@sign_in_bp.post('/sign-in/verify-otp')
def login_for_2fa():
    header = request.headers.get("Authorization")
    if not header:
        return {"error": "Sign in is required."}
    try:
        payload = decode_jwt_token(header)
        if not payload["is_2fa"]:
            return {"error": "Access Denied."}
        data = request.get_json()
        totp_token = data.get("otp")
        if not totp_token:
            return {"error": "OTP Required."}
        user = sign_in(payload["email"])
        stored_password, stored_role, is_active, name, blacklist, is_2fa = user
        verification = verify_totp(payload["email"], totp_token)
        if not verification:
            return jsonify({"error": "Invalid otp"}), 400
        return {"message": "Valid OTP. Login sucessful.", "token": generate_login_jwt_token(name, payload["email"], stored_role, is_active, blacklist)}
    except Exception as e:
        # raise e
        return jsonify({"error": str(e)}), 400