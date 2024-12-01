from flask import jsonify, Blueprint, request
from utils.jwt_utils import decode_jwt_token
from user import *

activate_data = Blueprint('activate_data', __name__)
@activate_data.get('/activate')
def activate_data_endpoint():
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Missing token"}), 400
    try:
        payload = decode_jwt_token(token)
        activate_user(payload["email"])
        return jsonify({"message": "Email verified successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
