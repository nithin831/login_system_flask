import requests
from flask import jsonify, Blueprint, request, url_for
from user import *
from utils.jwt_utils import *

auth_github = Blueprint('auth_github', __name__)

@auth_github.get('/auth')
def github_login():
    """Redirects the user to GitHub's authorization page."""
    redirect_url = Config.FRONTEND_URL + url_for('auth_github.github_callback')
    auth_url = f"{Config.GITHUB_AUTH_URL}?client_id={Config.GITHUB_CLIENT_ID}&redirect_uri={redirect_url}&scope=user"
    return jsonify({"url":auth_url}), 200

@auth_github.get('/auth/callback')
def github_callback():
    """Handles the callback from GitHub and processes the login."""
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "Authorization code not provided"}), 400
    # Exchange the authorization code for an access token
    token_response = requests.post(
        Config.GITHUB_TOKEN_URL,
        headers={'Accept': 'application/json'},
        data={
            'client_id': Config.GITHUB_CLIENT_ID,
            'client_secret': Config.GITHUB_CLIENT_SECRET,
            'code': code
        }
    )
    if token_response.status_code != 200:
        return jsonify({"error": "Failed to fetch access token from GitHub"}), 400
    token_data = token_response.json()
    # print(token_data)
    access_token = token_data.get('access_token')
    # print(access_token)
    if not access_token:
        return jsonify({"error": "Access token not received"}), 400
    # Fetch the user data from GitHub
    user_response = requests.get(
        Config.GITHUB_API_URL,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    if user_response.status_code != 200:
        return jsonify({"error": "Failed to fetch user data from GitHub"}), 400
    user_data = user_response.json()
    # print(user_data)
    email = user_data.get('email')
    if not email:
        return jsonify({"error": "Email not provided by GitHub"}), 400
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
        token = generate_login_jwt_token(user["name"], email, user["role"], user["is_active"], user["blacklist"], user["is_2fa"], type="login")
        return jsonify({"message": "Login successful", "token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        # raise e








