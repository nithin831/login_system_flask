from flask import jsonify, send_file
from utils.totp_utils import *
from user import *
from utils.jwt_utils import decode_verification_token

def qr_code(token):
    if not token:
        return jsonify({"error": "Missing token"}), 400
    try:
        email = decode_verification_token(token)
        secret = fetch_secret_key(email)
        if not secret:
            return jsonify({"error": "QR code not available. Please login first."}), 400

        # Generate QR code
        qr_code_img = generate_qr_code(secret[0], email)

        return send_file(qr_code_img, mimetype='image/png', as_attachment=False, download_name='totp-qr.png')
    except Exception as e:
        return {"error": str(e)}