from flask import jsonify, Blueprint, request
from utils.jwt_utils import generate_verification_token
from utils.email_utils import send_reset_password_email
from config import Config
from user import *
from validate import *

request_pwd_reset = Blueprint('request_pwd_reset', __name__)
@request_pwd_reset.post('/request-password-reset')
def request_password_reset():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    try:
        validate_user_email(email)
        user = check_user_exist(data)
        if user:
            is_active, is_blacklisted = user
            if is_blacklisted:
                return jsonify({"error": "This email address is blacklisted, Please contact support."}), 400
            if not is_active:
                return jsonify({"error": "User not found"}), 404
        else:
            return jsonify({"error": "User not found"}), 404

        # Generate password reset token
        reset_token = generate_verification_token(email)

        # Send the password reset email
        reset_link = f"{Config.FRONTEND_URL}/reset-password?token={reset_token}"
        send_reset_password_email(email, reset_link)

        return jsonify({"message": "Password reset email has been sent. Please check your inbox."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

