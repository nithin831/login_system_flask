from flask import Flask, request, jsonify
from utils.blacklist_utils import blacklist_user

def blacklist_user_endpoint(data):
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required."}), 400
    # Call the function to blacklist the user
    result = blacklist_user(email)
    if "error" in result:
        return jsonify(result), 404  # Not found if user doesn't exist
    return jsonify(result), 200  # Success response if user was blacklisted
