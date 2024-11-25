from flask import Flask, request, jsonify
from user import change_password_logic, check_user_exist
from validate import change_password_validate


def change_password_route(data):
    user = check_user_exist(data)
    if user:
        is_active, is_blacklisted = user
        if is_blacklisted:
            return jsonify({"error": "This email address is blacklisted, Please contact support."}), 400
        if not is_active:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "User not found"}), 404
    if not data:
        return jsonify({"error": "Invalid input. JSON payload is required.or enter the user details"}), 400
    validate = change_password_validate(data)
    if validate:
        return validate
    email = data.get('email')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    # Calling the password  logic
    response = change_password_logic(email, current_password, new_password)
    return jsonify(response)




