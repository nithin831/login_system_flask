from flask import jsonify
from user import *
from validate import *

def blacklist_user_endpoint(data):
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required."}), 400
    try:
        validate_user_email(email)
        # Call the function to blacklist the user
        result = blacklist_user(email)
        if "error" in result:
            return jsonify(result), 404  # Not found if user doesn't exist
        return jsonify(result), 200  # Success response if user was blacklisted
    except Exception as e:
        return {"error": str(e)}