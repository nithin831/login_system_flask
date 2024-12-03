from flask import jsonify, Blueprint, request
from user import *
from utils.auth_check import is_admin
from validate import *
from utils.email_utils import send_create_user_email_from_admin, send_account_update_email

admin = Blueprint('admin', __name__)
@admin.patch('/blacklist/email')
@is_admin
def blacklist_endpoint():
    try:
        data = request.get_json()
        email = data.get("email")
        if not email:
            return jsonify({"error": "Email is required."}), 400
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

@admin.post('/create-user')
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

@admin.get('/fetch-users')
@is_admin
def get_users():
    try:
        page = request.args.get('page', 1)
        per_page = request.args.get('per_page', 10)
        is_valid, error_message = validate_pagination(page, per_page)
        if not is_valid:
            return jsonify({'message': error_message}), 400
        page = int(page)
        per_page = int(per_page)
        email = request.args.get('email')
        name = request.args.get('name')
        role = request.args.get('role')
        is_active = request.args.get('is_active')
        search = request.args.get('search')
        users,total_count = fetch_users_from_db(page, per_page, email, name, role, is_active, search)
        # Handle the case where no users match the filters
        if not users:
            return jsonify({
                "message": "No users found matching the given criteria."
            }), 404
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
            # Construct paginated response
        response = {
            "total_count": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page,
            "users": user_list
            }
        # print(user_list)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching users: {e}'}), 500

@admin.patch('/update-user')
@is_admin
def update_users():
    try:
        data = request.json
        email = data.get("email")
        name = data.get("name")
        password = data.get("password")
        role = data.get("role")
        print(role)
        is_active = data.get("is_active")
        # Validate input
        if not email:
            return jsonify({"error": "Email is required to update the user."}), 400
        response, message = validate_user_email(email)
        if not response:
            return jsonify({"message": message})
        # Create a dictionary of the fields to update
        update_fields = {}
        if name:
            response, message = validate_user_name(name)
            if not response:
                return jsonify({"message": message})
            update_fields["name"] = name
        if password:
            response, message = validate_user_password(password)
            if not response:
                return jsonify({"message": message})
            # hashed_password = hash_password(password)  # Example hashing function
            update_fields["password"] = password
        if role:
            update_fields["role"] = role
        if is_active:
            update_fields["is_active"] = is_active
        # If no fields are provided to update, return an error
        if not update_fields:
            return jsonify({"error": "No update fields provided."}), 400
        # Update the user in the database
        update_user_details(email, update_fields)
        # Send an account update email
        send_account_update_email(email)
        return jsonify({"message": "User details updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while updating the user: {str(e)}"}), 500
