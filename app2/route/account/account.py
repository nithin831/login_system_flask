import requests
from flask import jsonify, Blueprint, request
import bcrypt
from config import Config
import pyotp
from user import *
from validate import *
from utils.jwt_utils import *
from utils.email_utils import *
from utils.auth_check import is_sign_in
from route.admin.admin import update_user

account = Blueprint('account', __name__)

@account.post('/user/register')
def register_user():
    data = request.get_json()
    role = "user"
    is_active = False
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    if not email or not password or not name:
        return jsonify({"error": "All fields are required"}), 400
    response, message = validate_user_email(email)
    if not response:
        return jsonify({"message": message}), 400
    response, message = validate_user_name(name)
    if not response:
        return jsonify({"message": message}), 400
    response, message = validate_user_password(password)
    if not response:
        return jsonify({"message": message}), 400
    # checks wheather the user exist or not
    try:
        user_record = check_user_exist(email)
        if not user_record:
            # If user is not found in database, then register
            create_user(email, password, name, role, is_active)  # Register the user
            # Generate a verification token and send it via email
            verification_token = generate_verification_jwt_token(email, type="activate_user")
            verification_link = f"{Config.FRONTEND_URL}/account/activate?token={verification_token}"
            send_verification_email(email, verification_link)
            return jsonify({"message": "User registered successfully. Please verify your email to complete the registration process."}), 201
        #  if user record is present in database
        if user_record["blacklist"]:
            return jsonify({"error": "This email address is blacklisted and cannot be used for registration, please contact support."}), 400
        if user_record["is_active"]:
            return jsonify({"error": "User is already registered."}), 400
        else:
            # If is_active is FALSE and email is not blacklisted, proceed with registration, with the given data by updating the existing data in the database
            update_user(email, password, name, role, is_active)
            # Generate a verification token and send it via email
            verification_token = generate_verification_jwt_token(email, type="activate_user")
            verification_link = f"{Config.FRONTEND_URL}/account/activate?token={verification_token}"
            send_verification_email(email, verification_link)
            return jsonify({"message": "User registered successfully. Please verify your email to complete the registration process."}), 201
    except Exception as e:
        # raise e
        return jsonify({"error": str(e)}), 500

@account.post('/admin/register')
def register_admin():
    data = request.get_json()
    role = "admin"
    is_active = False
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    if not email or not password or not name:
        return jsonify({"error": "All fields are required"}), 400
    response, message = validate_user_email(email)
    if not response:
        return jsonify({"message": message}), 400
    response, message = validate_user_name(name)
    if not response:
        return jsonify({"message": message}), 400
    response, message = validate_user_password(password)
    if not response:
        return jsonify({"message": message}), 400
    # checks wheather the user exist or not
    try:
        user_record = check_user_exist(email)
        if not user_record:
            # If user is not found in database, then register
            create_user(email, password, name, role, is_active)  # Register the user
            # Generate a verification token and send it via email
            verification_token = generate_verification_jwt_token(email, type="activate_user")
            verification_link = f"{Config.FRONTEND_URL}/account/activate?token={verification_token}"
            send_verification_email(email, verification_link)
            return jsonify({"message": "User registered successfully. Please verify your email to complete the registration process."}), 201
        #  if user record is present in database
        if user_record["blacklist"]:
            return jsonify({"error": "This email address is blacklisted and cannot be used for registration, please contact support."}), 400
        if user_record["is_active"]:
            return jsonify({"error": "User is already registered."}), 400
        else:
            # If is_active is FALSE and email is not blacklisted, proceed with registration, with the given data by updating the existing data in the database
            update_user(email, password, name, role, is_active)
            # Generate a verification token and send it via email
            verification_token = generate_verification_jwt_token(email, type="activate_user")
            verification_link = f"{Config.FRONTEND_URL}/account/activate?token={verification_token}"
            send_verification_email(email, verification_link)
            return jsonify({"message": "User registered successfully. Please verify your email to complete the registration process."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@account.get('/activate')
def activate_data_endpoint():
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Missing token"}), 400
    try:
        payload = decode_jwt_token(token)
        if payload.get('type') != "activate_user":
            return jsonify({"error": "Invalid permission."}), 404
        activate_user(payload["email"])
        return jsonify({"message": "Email verified successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@account.post('/resend-activation')
def resend_activation():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    response, message = validate_user_email(email)
    if not response:
        return jsonify({"message": message})
    try:
        user = check_user_exist(email)
        if user:
            if user['blacklist']:
                return jsonify({"error": "This email address is blacklisted and cannot recieve the verification mail, please contact support."}), 400
            if user["is_active"]:
                return jsonify({"message": "This account is already verified, Sign in with email and password."}), 400
        else:
            return jsonify({"error": "No User found, Please register again!"}), 404
        # Generate a new verification token
        verification_token = generate_verification_jwt_token(email, type="activate_user")
        verification_link = f"{Config.FRONTEND_URL}/account/activate?token={verification_token}"
        # Send the verification email
        send_verification_email(email, verification_link)
        return jsonify({"message": "A new activation email has been sent. Please check your inbox."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@account.post('/request-password-reset')
def request_password_reset():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    response, message = validate_user_email(email)
    if not response:
        return jsonify({"message": message})
    try:
        user = check_user_exist(email)
        if user:
            is_active, is_blacklisted = user
            if user["blacklist"]:
                return jsonify({"error": "This email address is blacklisted, Please contact support."}), 400
            if not user["is_active"]:
                return jsonify({"error": "User not found"}), 404
        else:
            return jsonify({"error": "User not found"}), 404
        # Generate password reset token
        reset_token = generate_verification_jwt_token(email, type="reset_password")
        # Send the password reset email
        reset_link = f"{Config.FRONTEND_URL}/account/reset-password?token={reset_token}"
        send_reset_password_email(email, reset_link)
        return jsonify({"message": "Password reset email has been sent. Please check your inbox."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@account.post('/reset-password')
def reset_password_endpoint():
    token = request.args.get('token')
    data = request.get_json()
    new_password = data.get('new_password')
    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400
    response, message = validate_user_password(new_password)
    if not response:
        return jsonify({"message": message})
    try:
        payload = decode_jwt_token(token)  # Decode the token to get email
        if payload.get('type') != "reset_password":
            return jsonify({"error": "Invalid permission."}), 404
        update_new_password(new_password, payload["email"])
        return jsonify({"message": "Password has been reset successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@account.post('/sign-in')
def login():
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
        # Check if user is active
        if user["blacklist"]:
            return jsonify({"error": "User is Blacklisted. Please contact support."}), 400
        if not user["is_active"]:
            return jsonify({"error": "User not found."}), 400
        # Validate the password
        if not request.args.get("otp") and user["is_2fa"]:
            return {"message": "Enter the OTP from the Authenticator App."}, 200
        if request.args.get("otp") and user["is_2fa"]:
            totp_token = request.args.get("otp")
            verification = verify_totp(email, totp_token)
            if not verification:
                return jsonify({"error": "Invalid otp"}), 400
        if not bcrypt.checkpw(password.encode('utf-8'), user["password"].tobytes()):
            return jsonify({"error": "User not found or incorrect credentials."}), 400
        return {"message": "Valid OTP. Login sucessful.",
             "token": generate_login_jwt_token(user["name"], email, user["role"], user["is_active"], user["blacklist"], user["is_2fa"], type="login")}

    except Exception as e:
        # raise e
        return jsonify({"error": str(e)}), 400

@account.get('/fetch-data')
def get_details():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Sign in is required."}), 400
    try:
        # Check the token and retrieve user details
        payload = decode_jwt_token(token)
        if payload.get('type') != "login":
            return jsonify({"error": "Invalid permission."}), 404
        return jsonify({
            "email": payload["email"],
            "name": payload["name"],
            "role": payload["role"]
        }), 200
    except Exception as e:
        # raise e
        return jsonify({"error": str(e)}), 400

@account.post('/change-password')
@is_sign_in
def change_password_route(email):
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    if not current_password or not new_password:
        return {"error": "Current password, and new password are required."}, 400
    response, message = validate_user_password(new_password)
    if not response:
        return jsonify({"message": message})
    if new_password == current_password:
        return jsonify({"error": "New password must be different"}), 404
    try:
        stored_password = fetch_password(email)
        # Validate the current password
        if not bcrypt.checkpw(current_password.encode('utf-8'), stored_password["password"].tobytes()):
            return jsonify({"error": "Current password is incorrect."}), 401
        # Update the password in the database
        update_new_password(new_password, email)
        return jsonify({"message": "Password updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@account.post('/2fa/enable-2fa')
@is_sign_in
def enable_2fa(email):
    try:
        if request.args.get("otp"):
            totp_token = request.args.get("otp")
            verification = verify_totp(email, totp_token)
            if not verification:
                 return jsonify({"error": "Invalid otp"}), 400
            update_2fa(True, email)
            return {"message": "Valid OTP. 2 Step Authentication is enabled sucessfully."}
        secret = pyotp.random_base32()
        update_secret_key(secret,  email)
        url = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name='login App')
        return {
            "message": "Please use your secret key or scan the QR code from the authenticator app and Enter the otp to enable the 2 step Authentication.",
            "key": secret, "qr_link": f"https://quickchart.io/qr?text={url}"}
    except Exception as e:
        # raise e
        return jsonify({"error": str(e)}), 400

@account.post('/2fa/disable-2fa')
@is_sign_in
def disable_2fa(email):
    try:
        data = request.get_json()
        totp_token = data.get('totp_token')
        if not totp_token:
            return {"error": "Please enter otp."}
        verification = verify_totp(email, totp_token)
        if not verification:
            return jsonify({"error": "Invalid otp"}), 400
        is_2fa = False
        update_2fa(is_2fa, email)
        return {"message": "Valid OTP. 2 Step Authentication is disabled sucessfully."}
    except Exception as e:
        return jsonify({"error": str(e)}), 400
