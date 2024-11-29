import pyotp
from flask import jsonify, Blueprint
from user import update_secret_key
from utils.auth_check import is_sign_in

secret_key = Blueprint('secret_key', __name__)
@secret_key.post('/2fa/secret-key/generation')
@is_sign_in
def secret_key_gen(email):
    try:
        secret = pyotp.random_base32()
        update_secret_key(secret, email)
        url = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name='login App')
        return {"message": "Please use your secret key or scan the QR code from the authenticator app and Enter the otp to enable the 2 step Authentication.","key":secret, "qr_link": f"https://quickchart.io/qr?text={url}"}
    except Exception as e:
        return jsonify({"error": str(e)}), 400