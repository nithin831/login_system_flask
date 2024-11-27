from flask import jsonify
from utils.totp_utils import *
from user import *
from utils.jwt_utils import *

def verify_totp(token, data):
    totp_token = data.get('totp_token')
    if not token or not totp_token:
        return jsonify({"error": "Please enter the TOTP"}), 400
    try:
        email = decode_verification_token(token)
        user = sign_in(email)
        user_id, stored_password, stored_role, is_active, name, blacklist, secret = user
        # Validate the TOTP token
        if validate_totp(secret, totp_token):
            # Generate JWT using the utility function
            token = generate_jwt(user_id, name, email, stored_role, is_active, blacklist)
            return jsonify({"message": "login sucessfull", "token":token }), 200
        else:
            return jsonify({"error": "Invalid TOTP token"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400