from functools import wraps
import bcrypt
import jwt
from flask import request, jsonify, Blueprint, Response
from config import Config
from user import fetch_sign_in
from validate import verify_totp, validate_user_email


def is_sign_in(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        header = request.headers.get("Authorization")
        if not header:
            return {"error": "Sign in is required."}
        try:
            payload = jwt.decode(header, Config.SECRET_KEY, algorithms=["HS256"])
            if payload.get('type') != "login":
                return jsonify({"error": "Invalid permission."}), 404
            result = func(*args, email=payload["email"], **kwargs)
            return result
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired."}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token."}
    return decorator

def is_admin(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        header = request.headers.get("Authorization")
        # print(header)
        if not header:
            return {"error": "Sign in is required."}
        try:
            payload = jwt.decode(header, Config.SECRET_KEY, algorithms=["HS256"])
            # print((payload))
            role = payload["role"]
            if role == "admin":
                result = func(*args, **kwargs)
                return result
            return {"message":"Permission denied"}
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired."}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token."}
    return decorator

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # # Get email and password from request
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400
        response, message = validate_user_email(email)
        if not response:
            return jsonify({"message": message})
        try:
            user = fetch_sign_in(email)
            if not user:
                return jsonify({"error": "User not found."}), 400
            if user["blacklist"]:
                return jsonify({"error": "User is Blacklisted. Please contact support."}), 400
            if not user["is_active"]:
                return jsonify({"error": "User not found."}), 400
            # Handle 2FA if applicable
            if user["is_2fa"]:
                otp = request.args.get("otp")
                if not otp:
                    return jsonify({"message": "Enter the OTP from the Authenticator App."}), 200
                # Verify OTP
                verification = verify_totp(email, otp)
                if not verification:
                    return jsonify({"error": "Invalid OTP"}), 400
            # Validate password
            if not bcrypt.checkpw(password.encode('utf-8'), user["password"].tobytes()):
                return jsonify({"error": "Incorrect credentials."}), 400
            # Call the original function after successful validation, passing user and email
            return func(*args, **kwargs, user=user, email=email)
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return decorated_function






