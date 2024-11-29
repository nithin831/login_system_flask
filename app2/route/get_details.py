from flask import jsonify, Blueprint, request
from utils.jwt_utils import get_user_details_from_jwt

fetch = Blueprint('fetch', __name__)
@fetch.get('/fetch')
def get_details():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Authorization token required."}), 401
    
    # Remove "Bearer " prefix if it's present in the token header
    token = token.replace("Bearer ", "")

    # Check the token and retrieve user details
    result = get_user_details_from_jwt(token)
    
    if "error" in result:
        return jsonify(result), 401  # Unauthorized if token is invalid or session expired

    # Return user details if the token is valid
    return jsonify(result), 200