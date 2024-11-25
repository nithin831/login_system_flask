from flask import request, jsonify
from user import *
from validate import validate_user_data

def register_user(data, role):
    # Validate user data
    validation_response = validate_user_data(data)
    if validation_response:
        return validation_response  # Return validation error response if any
    # print(data)
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    if not email or not password or not name:
        return jsonify({"error": "All fields are required"}), 400
    try:  
        # checks wheather the user exist or not
        check = check_user_exist(data)
        if not check:
            # If is_active is FALSE and email is not blacklisted, proceed with registration
            create_user(email, password, name, role) # Register the user
            return jsonify({"message": "User registered successfully. Please verify your email to complete the registration process."}), 201
        return jsonify(check), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
