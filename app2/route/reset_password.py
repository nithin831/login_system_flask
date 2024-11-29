from flask import jsonify, Blueprint, request
from utils.jwt_utils import decode_verification_token
from user import *
from validate import *

reset_password = Blueprint('reset_password', __name__)
@reset_password.post('/reset-password')
def reset_password_endpoint():
    token = request.args.get('token')
    data = request.get_json()
    new_password = data.get('new_password')
    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400
    try:
        validate_user_password(new_password)
        email = decode_verification_token(token)  # Decode the token to get email
        update_new_password(new_password, email)
        return jsonify({"message": "Password has been reset successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    
