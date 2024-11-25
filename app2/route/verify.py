from flask import jsonify
from database import get_connection, release_connection
from utils.jwt_utils import decode_verification_token

def verify_user(token):
    if not token:
        return jsonify({"error": "Missing token"}), 400

    try:
        email = decode_verification_token(token)
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE user_table SET is_active = TRUE WHERE email = %s", (email,))
            conn.commit()
            return jsonify({"message": "Email verified successfully!"}), 200
        finally:
            release_connection(conn)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
