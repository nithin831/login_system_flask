from flask import Blueprint, jsonify, request, redirect, url_for
import requests
from config import Config
from user import create_user, check_user_exist, fetch_sign_in
from utils.jwt_utils import generate_login_jwt_token

auth_facebook = Blueprint('auth_facebook', __name__)

# Facebook Login Route
@auth_facebook.get('/auth')
def facebook_login():
    redirect_url = Config.FRONTEND_URL + url_for('auth_facebook.facebook_callback')
    facebook_auth_url = (
        f"{Config.FACEBOOK_AUTH_URL}?client_id={Config.FACEBOOK_CLIENT_ID}&redirect_uri={redirect_url}&scope=email,public_profile"
    )
    return jsonify({"url":facebook_auth_url}), 200

# Facebook Callback Route
@auth_facebook.get('/auth/callback')
def facebook_callback():
    code = request.args.get('code')
    redirect_url = Config.FRONTEND_URL + url_for('auth_facebook.facebook_callback')
    if not code:
        return jsonify({"error": "Authorization code is missing."}), 400
    # Exchange code for an access token
    token_params = {
        "client_id": Config.FACEBOOK_CLIENT_ID,
        "client_secret": Config.FACEBOOK_CLIENT_SECRET,
        "redirect_uri": redirect_url,
        "code": code,
    }
    token_response = requests.get(Config.FACEBOOK_TOKEN_URL, params=token_params)
    token_data = token_response.json()
    if "error" in token_data:
        return jsonify({"error": token_data["error"]}), 400
    access_token = token_data.get("access_token")
    # Fetch user data from Facebook
    user_info_params = {
        "fields": "id,name,email",
        "access_token": access_token,
    }
    user_info_response = requests.get(Config.FACEBOOK_API_URL, params=user_info_params)
    user_data = user_info_response.json()
    if "error" in user_data:
        return jsonify({"error": user_data["error"]}), 400
    email = user_data.get("email")
    if not email:
        return jsonify({"error": "Email is required but not provided by Facebook."}), 400
    # Check if the user exists in the database
    try:
        user = fetch_sign_in(email)
        if not user:
            return jsonify({"message": "User not registered."}), 201
        if user["blacklist"]:
            return jsonify({"error": "User is blacklisted. Please contact support."}), 400
        if not user["is_active"]:
            return jsonify({"error": "User is inactive. Please verify your account."}), 400
        # Generate JWT token for existing user
        token = generate_login_jwt_token(user["name"], email, user["role"], user["is_active"],
                                         user["blacklist"], user["is_2fa"])
        return jsonify({"message": "Login successful", "token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        # raise e