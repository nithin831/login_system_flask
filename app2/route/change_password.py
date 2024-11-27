from flask import jsonify
from user import change_password_logic, check_user_exist
from validate import *

def change_password_route(data):
    # print(data)
    email = data.get('email')
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    if not email or not current_password or not new_password:
        return {"error": "Email, current password, and new password are required."}, 400
    try:
        validate_user_email(email)
        validate_user_password(new_password)
        user = check_user_exist(data)
        if user:
            is_active, is_blacklisted = user
            if is_blacklisted:
                return jsonify({"error": "This email address is blacklisted, Please contact support."}), 400
            if not is_active:
                return jsonify({"error": "User not found"}), 404
        else:
            return jsonify({"error": "User not found"}), 404
        # Calling the password  logic
        if new_password == current_password:
            return jsonify({"error": "New password must be different"}), 404
        response = change_password_logic(email, current_password, new_password)
        return jsonify(response),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





