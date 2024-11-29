from flask import jsonify, Blueprint, request
from user import update_2fa
from utils.auth_check import is_sign_in
from validate import verify_totp

disable_auth = Blueprint('disable_auth', __name__)
@disable_auth.post('/2fa/disable-2fa')
@is_sign_in
def disable_2fa(email):
    data = request.get_json()
    totp_token = data.get('totp_token')
    if not totp_token:
        return {"error": "Please enter otp."}
    try:
        verification = verify_totp(email, totp_token)
        if not verification:
            return jsonify({"error": "Invalid otp"}), 400
        is_2fa = False
        update_2fa(is_2fa, email)
        return {"message": "Valid OTP. 2 Step Authentication is disabled sucessfully."}
    except Exception as e:
        return jsonify({"error": str(e)}), 400

