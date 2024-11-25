from flask import request, jsonify
from database import get_connection, release_connection
from utils.jwt_utils import generate_verification_token
from utils.email_utils import send_verification_email
from config import Config

def resend_activation(data):
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT is_active, blacklist FROM user_table WHERE email = %s", (email,))
            user = cur.fetchone()

            if not user:
                return jsonify({"error": "Please register agian!"}), 404

            is_active, is_blacklisted = user

            if is_blacklisted:
                return {"error": "This email address is blacklisted and cannot recieve the verification mail, please contact support."}
            if is_active:
                return jsonify({"message": "This account is already verified, Sign in with email and password."}), 400

            # Generate a new verification token
            verification_token = generate_verification_token(email)
            verification_link = f"{Config.FRONTEND_URL}/verify?token={verification_token}"

            # Send the verification email
            send_verification_email(email, verification_link)

            return jsonify({"message": "A new activation email has been sent. Please check your inbox."}), 200
    finally:
        release_connection(conn)
