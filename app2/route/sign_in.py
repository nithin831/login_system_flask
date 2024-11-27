import bcrypt
from flask import jsonify
from user import *
from validate import *
from utils.jwt_utils import generate_jwt, generate_verification_token
# from utils.redis_utils import test_redis_connection

# Check Redis connection before processing sign-in
# test_redis_connection()

def login(data):
    # print(data)
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400
    try:
        validate_user_email(email)
        user = sign_in(email)
        if not user:
            return jsonify({"error": "User not found."}), 400
        user_id, stored_password, stored_role, is_active, name, blacklist, secret_key = user
        # Check if user is active
        if blacklist:
            return jsonify({"error": "User is Blacklisted. Please contact support."}), 400
        if not is_active:
            return jsonify({"error": "User not found."}), 400
        # Validate the password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.tobytes()):
            # If TOTP is not enabled, generate QR code for first-time setup
            if not secret_key:
                secret_key = generate_totp_secret()
                update_secret_key(secret_key, email)
            token = generate_verification_token(email)
            # Store JWT in Redis with expiration
            # redis_key = f"jwt:{user_id}"
            # redis_client.setex(redis_key, Config.JWT_EXPIRATION_SECONDS, token)
            return jsonify({
                "message": "Please enter the OTP from your authenticator app if already scanned, otherwise Scan the QR code to set up TOTP authentication.",
                "enter_otp_link": f"/verify-totp?token={token}",
                "qr_code_link": f"/qr-code?token={token}",
                "note": "After scaning QR code, please do sign in again."}), 200
        else:
            return jsonify({"error": "User not found or incorrect credentials."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400