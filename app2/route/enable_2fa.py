import pyotp
from flask import jsonify, Blueprint, request
from user import update_2fa, update_secret_key
from utils.auth_check import is_sign_in
from validate import verify_totp

enable_auth = Blueprint('enable_auth', __name__)
@enable_auth.post('/2fa/enable-2fa')
@is_sign_in
def enable_2fa(email):
    try:
        if request.args.get("otp"):
            totp_token = request.args.get("otp")
            verification = verify_totp(email, totp_token)
            if not verification:
                 return jsonify({"error": "Invalid otp"}), 400
            update_2fa(True, email)
            return {"message": "Valid OTP. 2 Step Authentication is enabled sucessfully."}
        secret = pyotp.random_base32()
        update_secret_key(secret,  email)
        url = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name='login App')
        return {
            "message": "Please use your secret key or scan the QR code from the authenticator app and Enter the otp to enable the 2 step Authentication.",
            "key": secret, "qr_link": f"https://quickchart.io/qr?text={url}"}
    except Exception as e:
        # raise e
        return jsonify({"error": str(e)}), 400
