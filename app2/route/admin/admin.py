from flask import jsonify, Blueprint, request
from user import *
from utils.auth_check import is_admin
from validate import *
from user import check_user_exist, blacklist_mail
from validate import validate_user_email
from user import create_user
from utils.email_utils import send_create_user_email_from_admin
from user import update_user
from validate import validate_pagination
from user import fetch_users_from_db
from utils.email_utils import send_account_update_email
from validate import validate_user_name, validate_user_password

admin = Blueprint('admin', __name__)
@admin.patch('/blacklist/email')
@is_admin
def blacklist_endpoint():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required."}), 400
    try:
        response, message = validate_user_email(email)
        if not response:
            return jsonify({"message": message}), 400
        if not check_user_exist(data):
            return jsonify({"error": "User not found."}), 400
        # Call the function to blacklist the user
        blacklist_mail(email)
        return {"message": f"User with email {email} has been blacklisted."}
    except Exception as e:
        return {"error": str(e)}

@admin.post('/create')
@is_admin
def create_user_by_admin():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')
        is_active = True

        if not name or not email or not password:
            return jsonify({"error": "Name, email, and password are required"}), 400

        for validator, value in [
            (validate_user_email, email),
            (validate_user_name, name),
            (validate_user_password, password),
        ]:
            response, message = validator(value)
            if not response:
                return jsonify({"message": message})
        existing_user=check_user_exist(data)
        if existing_user:
            return jsonify({"error": "User with this email already exists."}), 400
        create_user(email, password, name, role, is_active)
        send_create_user_email_from_admin(email,name,password)
        print(send_create_user_email_from_admin)
        return jsonify({"message": "User created successfully and mail has been sent to the user" ,"user": {
            "email": email,
            "name": name,
            'role': role,
            'is_active': is_active
        }}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating users: {e}'}), 500

@admin.get('/fetch_users')
@is_admin
def get_users():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    is_valid, error_message = validate_pagination(page, per_page)
    if not is_valid:
        return jsonify({'message': error_message}), 400
    try:
        page = int(page)
        per_page = int(per_page)
        email = request.args.get('email')
        name = request.args.get('name')
        role = request.args.get('role')
        is_active = request.args.get('is_active')
        search = request.args.get('search')
        users = fetch_users_from_db(page, per_page, email, name, role, is_active, search)
        # Transform the result into JSON
        user_list = []
        for user in users:

            # Convert memoryview fields to strings (if any)
            user_dict = {
                "id": user[0],
                "email": user[1],
                "name": user[3],
                "role": user[4],
                "created_on": user[5],
                "is_active": user[6],
                "blacklist": user[7]
            }
            # Handle any memoryview or bytea fields
            for key, value in user_dict.items():
                if isinstance(value, memoryview):  # Convert memoryview to string
                    user_dict[key] = value.tobytes().decode('utf-8')
            user_list.append(user_dict)
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching users: {e}'}), 500


@admin.patch('update_user')
@is_admin
def update_users():
    data = request.json
    email = data.get("email")
    name = data.get("name")
    password = data.get("password")
    role = data.get("role")
    try:
        if not email:
            return jsonify({"error": "Email is required to update the user."}), 400
        update_user(email, password,name, role)
        # Send the verification email
        send_account_update_email(email, name)
        return jsonify({"message": "User updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while updating the user.{str(e)}"}), 500
        # raise e

