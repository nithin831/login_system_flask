# @app.route('/admin/user', methods=['PATCH'])
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from route.admin.admin_middleware import admin_required
from user import check_user_exist


# PATCH /admin/user HTTP/1.1
# Host: yourdomain.com
# Authorization: Bearer <JWT_TOKEN>
# Content-Type: application/json
#
# {
#     "email": "admin@example.com", or user_id
#     "password": "newpassword123",
#     "role": "admin"
# }

@app.route('/admin/user', methods=['PATCH'])
@admin_required
def update_user():
    # Get the current admin user details from the JWT
    current_user = get_jwt_identity()  # Admin info (this is already authenticated)

    # Get user data to be updated from the request body
    data = request.get_json()
    user_id = data.get('user_id')  # The ID of the user to update
    email = data.get('email')  # The email of the user to update
    name = data.get('name')  # Name to update
    role = data.get('role')  # Role to update
    password=data.get('password') #Password to update note that password should be in hashed format only

    # Ensure at least one identifier is provided (user_id or email)
    if not user_id and not email:
        return jsonify({"error": "Either user_id or email must be provided to identify the user."}), 400

    # Ensure at least one field (name, role) is provided for updating
    if not any([name, role]):
        return jsonify({"error": "At least one field (name, role) must be provided to update."}), 400
    user = check_user_exist(data)
    if not user:
        return jsonify({"error": "User not found."}), 404
    # Ensure that an admin cannot update their own role or password without re-authentication (optional)
    if current_user['id'] == user_id and (role or password):
        return jsonify({"error": "You cannot change your own role or password through this request."}), 403
    # If the current admin is trying to change another admin's password or role, allow it
    if current_user['role'] == 'admin' and user['role'] == 'admin':
        # Ensure the admin doesn't change their own password or role
        if current_user['id'] == user['id']:
            return jsonify({"error": "You cannot change your own role or password."}), 403

    # # If email is provided, ensure it's unique if changed
    # if email:
    #     cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    #     existing_user = cursor.fetchone()
    #     if existing_user and existing_user['id'] != user['id']:  # Prevent changing email to an existing one
    #         conn.close()
    #         return jsonify({"error": "Email is already in use by another user."}), 400
    result=update_user(email, password, name, role)
    # # Prepare the update query
    # update_query = "UPDATE users SET"
    # update_values = []
    #
    # if name:
    #     update_query += " name = %s,"
    #     update_values.append(name)
    # if role:
    #     update_query += " role = %s,"
    #     update_values.append(role)
    #
    # # Remove the trailing comma
    # update_query = update_query.rstrip(',')
    #
    # # Add condition for identifying the user (by user_id or email)
    # if user_id:
    #     update_query += " WHERE id = %s"
    #     update_values.append(user_id)
    # elif email:
    #     update_query += " WHERE email = %s"
    #     update_values.append(email)
    #
    # # Execute the update query
    # cursor.execute(update_query, tuple(update_values))
    # conn.commit()
    # conn.close()
    return jsonify({
        "message": "User updated successfully",
        "updated_user_details": {result}
    }), 200
