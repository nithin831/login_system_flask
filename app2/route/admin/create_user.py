# from werkzeug.security import generate_password_hash
from flask import request, jsonify
from route.admin.admin_middleware import admin_required
from user import check_user_exist

# POST /admin/user HTTP/1.1
# Host: yourdomain.com
# Authorization: Bearer <JWT_TOKEN>
# Content-Type: application/json
#
# {
#     "name": "New User",
#     "email": "newuser@example.com",
#     "password": "password123",
#     "role": "user"
# }

# @app.route('/admin/user', methods=['POST'])
@admin_required
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')  # Default role is 'user'

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    existing_user=check_user_exist(data)

    if existing_user:
        return jsonify({"error": "User with this email already exists."}), 400

    new_user=create_user(email, password, name, role)
    return jsonify({"message": "User created successfully","user": new_user}), 201
