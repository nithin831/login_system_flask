from flask import jsonify
from database import get_connection, release_connection
from utils.jwt_utils import decode_verification_token
from user import *

def verify_user(token):
    if not token:
        return jsonify({"error": "Missing token"}), 400

    try:
        email = decode_verification_token(token)
        activate_user(email)
        return jsonify({"message": "Email verified successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
