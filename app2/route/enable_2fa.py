from flask import jsonify, Blueprint, request
from user import update_2fa
from utils.auth_check import is_sign_in
from validate import verify_totp

enable_auth = Blueprint('enable_auth', __name__)
@enable_auth.post('/2fa/enable-2fa')
@is_sign_in
def enable_2fa(email):
    data = request.get_json()
    totp_token = data.get('totp_token')
    if not totp_token:
        return {"error": "Please enter otp."}
    try:
        verification = verify_totp(email, totp_token)
        if not verification:
            return jsonify({"error": "Invalid otp"}), 400
        is_2fa = True
        update_2fa(is_2fa, email)
        return {"message": "Valid OTP. 2 Step Authentication is enabled sucessfully."}
    except Exception as e:
        # raise e
        return jsonify({"error": str(e)}), 400
