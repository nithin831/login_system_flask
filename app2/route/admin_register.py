from flask import jsonify, Blueprint, request
from user import *
from validate import *

admin_register = Blueprint('admin_register', __name__)
@admin_register.post('/admin/register')
def register_admin():
    data = request.get_json()
    role = "admin"
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    if not email or not password or not name:
        return jsonify({"error": "All fields are required"}), 400
    try:
        for validator, value in [
            (validate_user_email, email),
            (validate_user_name, name),
            (validate_user_password, password),
        ]:
            response, message = validator(value)
            if not response:
                return jsonify({"message": message})
        # checks wheather the user exist or not
        user_record = check_user_exist(data)
        if not user_record:
            # If user is not found in database, then register
            create_user(email, password, name, role)  # Register the user
            return jsonify({"message": "User registered successfully. Please verify your email to complete the registration process."}), 201
        #  if user record is present in database
        is_active, is_blacklisted = user_record
        if is_blacklisted:
            return jsonify({"error": "This email address is blacklisted and cannot be used for registration, please contact support."}), 400
        if is_active:
            return jsonify({"error": "User is already registered."}), 400
        else:
            # If is_active is FALSE and email is not blacklisted, proceed with registration, with the given data by updating the existing data in the database
            update_user(email, password, name, role)
            return jsonify({"message": "User registered successfully. Please verify your email to complete the registration process."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

