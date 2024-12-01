from flask import jsonify, Blueprint, request
from user import *
from utils.jwt_utils import generate_verification_jwt_token
from utils.email_utils import send_verification_email
from config import Config
from validate import *

resend_mail = Blueprint('resend_mail', __name__)
@resend_mail.post('/resend-activation')
def resend_activation():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    try:
        response, message = validate_user_email(email)
        if not response:
            return jsonify({"message": message})
        user = check_user_exist(data)
        if user:
            is_active, is_blacklisted = user
            if is_blacklisted:
                return jsonify({"error": "This email address is blacklisted and cannot recieve the verification mail, please contact support."}), 400
            if is_active:
                return jsonify({"message": "This account is already verified, Sign in with email and password."}), 400
        else:
            return jsonify({"error": "No User found, Please register again!"}), 404
        # Generate a new verification token
        verification_token = generate_verification_jwt_token(email)
        verification_link = f"{Config.FRONTEND_URL}/activate?token={verification_token}"
        # Send the verification email
        send_verification_email(email, verification_link)
        return jsonify({"message": "A new activation email has been sent. Please check your inbox."}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
