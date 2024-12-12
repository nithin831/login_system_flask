from flask import jsonify, Blueprint, request, url_for
from config import Config
from utils.jwt_utils import *
from utils.email_utils import send_login_link
from user import *
from validate import validate_user_email

passwordless = Blueprint('passwordless', __name__)

@passwordless.post('/login-request')
def request_login_link():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    # Validate email format
    response, message = validate_user_email(email)
    if not response:
        return jsonify({"message": message}), 400
    try:
        # Check if the user exists
        user = check_user_exist(email)
        if not user:
            return jsonify({"error": "User not found."}), 400
        # Check if user is active and blacklisted
        if user["blacklist"]:
            return jsonify({"error": "User is Blacklisted. Please contact support."}), 400
        if not user["is_active"]:
            return jsonify({"error": "User not found."}), 400
        # Generate a temporary login token
        login_token = generate_verification_jwt_token(email, type="login_request")
        login_link = f"{Config.FRONTEND_URL}{url_for('passwordless.login_callback')}?token={login_token}"
        # Send the login link via email
        send_login_link(email, login_link)
        return jsonify({"message": "Login link sent to your email."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@passwordless.get('/login/callback')
def login_callback():
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token is missing."}), 400
    try:
        # Decode the token to get the user's email
        payload = decode_jwt_token(token)
        email = payload.get('email')
        if payload.get('type') != "login_request":
            return jsonify({"error": "Invalid permission."}), 404
        # Fetch user details and Generate a new JWT for the user's session
        user = fetch_sign_in(email)
        return jsonify({
            "message": "Login successful.",
            "token": generate_login_jwt_token(user['name'], email, user['role'], user['is_active'], user['blacklist'], user['is_2fa'], type="login")
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

