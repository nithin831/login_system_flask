# from flask import request, jsonify, Blueprint
# import requests
# from user import check_user_exist, fetch_sign_in
# from utils.jwt_utils import generate_login_jwt_token
#
# auth_linkedin = Blueprint('auth_linkedin', __name__)
#
# # Configuration
# CLIENT_ID = "866lh50dprckek"
# CLIENT_SECRET = "WPL_AP1.3usOAzXhdQ7ZqpoF.I282wg=="
# REDIRECT_URI = "http://localhost:4000/auth_linkedin/linkedin/callback"
#
#
# @auth_linkedin.get('/linkedin')
# def linkedin_auth():
#     # Redirect user to LinkedIn's OAuth 2.0 authorization endpoint
#     auth_url = (
#         f"https://www.linkedin.com/oauth/v2/authorization?"
#         f"response_type=code&"
#         f"client_id={CLIENT_ID}&"
#         f"redirect_uri={REDIRECT_URI}&"
#         f"scope=profile,email,openid"
#     )
#     return jsonify({"auth_url": auth_url}), 200
#
#
# @auth_linkedin.get('/linkedin/callback')
# def linkedin_callback():
#     print("this is request args:",request.args)
#     # Retrieve authorization code
#     code = request.args.get('code')
#     print('this is code:',code)
#     if not code:
#         return jsonify({"error": "Missing authorization code"}), 400
#
#     # Exchange authorization code for access token
#     token_url = "https://www.linkedin.com/oauth/v2/accessToken"
#     token_data = {
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": REDIRECT_URI,
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#     }
#     token_response = requests.post(token_url, data=token_data)
#     print("this is token_response",token_response)
#     if token_response.status_code != 200:
#         return jsonify({"error": "Failed to exchange token"}), 400
#
#     token_info = token_response.json()
#     # print("this is token_info:",token_info)
#     access_token = token_info.get("access_token")
#     # print('this is access_token:',access_token)
#     if not access_token:
#         return jsonify({"error": "No access token received"}), 400
#
#     # Retrieve user information from LinkedIn
#     userinfo_url = "https://api.linkedin.com/v2/userinfo"
#     # email_url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
#     headers = {"Authorization": f"Bearer {access_token}"}
#     print(headers)
#
#
#     userinfo_response = requests.get(userinfo_url, headers=headers)
#     # print(userinfo_response)
#     user_info=userinfo_response.json()
#     email=user_info.get("email")
#     try:
#         user = fetch_sign_in(email)
#         if not user:
#             return jsonify({"message": "User not registered."}), 201
#         if user["blacklist"]:
#             return jsonify({"error": "User is blacklisted. Please contact support."}), 400
#         if not user["is_active"]:
#             return jsonify({"error": "User is inactive. Please verify your account."}), 400
#         # Generate JWT token for existing user
#         token = generate_login_jwt_token(user["name"], email, user["role"], user["is_active"], user["blacklist"],
#                                          user["is_2fa"])
#         return jsonify({"message": "Login successful", "token": token}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500





import requests
from flask import jsonify, Blueprint, request, url_for
from config import Config
from user import fetch_sign_in
from utils.jwt_utils import generate_login_jwt_token

auth_linkedin = Blueprint('auth_linkedin', __name__)

@auth_linkedin.get('/auth')
def linkedin_auth():
    """Redirects the user to LinkedIn's authorization page."""
    redirect_url = Config.FRONTEND_URL + url_for('auth_linkedin.linkedin_callback')
    auth_url = (
        f"{Config.LINKEDIN_AUTH_URL}"
        f"response_type=code&"
        f"client_id={Config.LINKEDIN_CLIENT_ID}&"
        f"redirect_uri={redirect_url}&"
        f"scope=profile,email,openid"
    )
    return jsonify({"url": auth_url}), 200


@auth_linkedin.get('/auth/callback')
def linkedin_callback():
    """Handles the callback from LinkedIn and processes the login."""
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "Authorization code not provided"}), 400
    redirect_url = Config.FRONTEND_URL + url_for('auth_linkedin.linkedin_callback')

    # Exchange the authorization code for an access token
    token_response = requests.post(
        Config.LINKEDIN_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_url,
            "client_id": Config.LINKEDIN_CLIENT_ID,
            "client_secret": Config.LINKEDIN_CLIENT_SECRET,
        },
    )

    if token_response.status_code != 200:
        return jsonify({"error": "Failed to fetch access token from LinkedIn"}), 400
    token_data = token_response.json()
    access_token = token_data.get('access_token')
    if not access_token:
        return jsonify({"error": "Access token not received"}), 400
    userinfo_url=Config.LINKEDIN_API_URL
    headers = {"Authorization": f"Bearer {access_token}"}
    print(headers)
    userinfo_response = requests.get(userinfo_url, headers=headers)
    # print(userinfo_response)
    user_info=userinfo_response.json()
    email=user_info.get("email")
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
                                         user["is_2fa"], type="login")
        return jsonify({"message": "Login successful", "token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500