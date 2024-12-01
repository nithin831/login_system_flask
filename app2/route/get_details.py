from flask import jsonify, Blueprint, request
from utils.jwt_utils import decode_jwt_token

fetch = Blueprint('fetch', __name__)
@fetch.get('/fetch')
def get_details():
    try:
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Sign in is required."}), 400
        # Check the token and retrieve user details
        payload = decode_jwt_token(token)
        return jsonify({
            "email": payload["email"],
            "name": payload["name"],
            "role": payload["role"]
        }), 200
    except Exception as e:
        # raise e
        return jsonify({"error": str(e)}), 400
