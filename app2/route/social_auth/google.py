import requests
from flask import jsonify, Blueprint, request, url_for
from config import Config
from user import fetch_sign_in
from utils.jwt_utils import generate_login_jwt_token

auth_google = Blueprint('auth_google', __name__)

@auth_google.get('/auth')
def google_login():
    """Redirects the user to Google's OAuth 2.0 authorization page."""
    redirect_url = Config.FRONTEND_URL + url_for('auth_google.google_callback')
    print(Config.FRONTEND_URL)
    auth_url = (
        f"{Config.GOOGLE_AUTH_URL}"
        f"client_id={Config.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={redirect_url}&"
        f"response_type=code&"
        f"scope=email profile"
    )
    return jsonify({"url": auth_url}), 200

@auth_google.get('/auth/callback')
def google_callback():
    """Handles the callback from Google and processes the login."""
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "Authorization code not provided"}), 400
    redirect_url = Config.FRONTEND_URL + url_for('auth_google.google_callback')
    # Exchange authorization code for access token
    token_response = requests.post(
        Config.GOOGLE_TOKEN_URL,
        data={
            "code": code,
            "client_id": Config.GOOGLE_CLIENT_ID,
            "client_secret": Config.GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_url,
            "grant_type": "authorization_code",
        },
    )
    if token_response.status_code != 200:
        return jsonify({"error": "Failed to fetch access token from Google"}), 400

    token_data = token_response.json()
    access_token = token_data.get('access_token')
    if not access_token:
        return jsonify({"error": "Access token not received"}), 400

    # Fetch the user data from Google
    user_response = requests.get(
        Config.GOOGLE_API_URL,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    if user_response.status_code != 200:
        return jsonify({"error": "Failed to fetch user data from Google"}), 400
    user_data = user_response.json()
    email = user_data.get('email')
    if not email:
        return jsonify({"error": "Email not provided by Google"}), 400
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
        token = generate_login_jwt_token(
            user["name"], email, user["role"], user["is_active"], user["blacklist"], user["is_2fa"], type="login"
        )
        return jsonify({"message": "Login successful", "token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
