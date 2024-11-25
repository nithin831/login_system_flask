
from flask import request, jsonify
from user import sign_in
# from utils.redis_utils import test_redis_connection

# Check Redis connection before processing sign-in
# test_redis_connection()

def login(data):
    # print(data)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    # Attempt to sign in
    result = sign_in(email, password)

    # Check for errors in the sign-in result
    if "error" in result:
        return jsonify(result), 401  # Unauthorized if sign-in fails

    # Success response
    return jsonify(result), 200  # OK if sign-in is successful
