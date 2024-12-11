from flask import  request, jsonify, Blueprint
import requests
from user import check_user_exist, fetch_sign_in
from utils.jwt_utils import  generate_login_jwt_token

auth_google = Blueprint('auth_google', __name__)
# Configuration
CLIENT_ID = "990501356456-39749cat7779klhf4ppjupaf21utnm6t.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:4000/auth_google/google/callback"

@auth_google.get('/google')
def google_auth():
    # Redirect user to Google's OAuth 2.0 authorization endpoint
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=email profile"
    )
    print(auth_url)
    return jsonify({"auth_url":auth_url}),


@auth_google.get('/google/callback')
def google_callback():
    # Retrieve authorization code
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "Missing authorization code"}), 400

    # Exchange authorization code for access token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(token_url, data=token_data)
    if token_response.status_code != 200:
        return jsonify({"error": "Failed to exchange token"}), 400

    token_info = token_response.json()
    access_token = token_info.get("access_token")
    if not access_token:
        return jsonify({"error": "No access token received"}), 400

    # Retrieve user information from Google
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(userinfo_url, headers=headers)
    if userinfo_response.status_code != 200:
        return jsonify({"error": "Failed to fetch user info"}), 400

    userinfo = userinfo_response.json()
    print(userinfo)
    email = userinfo.get("email")
    if not email:
        return jsonify({"error": "Failed to fetch email"}), 400

    try:
        user = fetch_sign_in(email)
        if not user:
            return jsonify({"message": "User not registered."}), 201
        if user["blacklist"]:
            return jsonify({"error": "User is blacklisted. Please contact support."}), 400
        if not user["is_active"]:
            return jsonify({"error": "User is inactive. Please verify your account."}), 400
        # Generate JWT token for existing user
        token = generate_login_jwt_token(user["name"], email, user["role"], user["is_active"], user["blacklist"],
                                         user["is_2fa"])
        return jsonify({"message": "Login successful", "token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
