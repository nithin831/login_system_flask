# app.route('/admin/user', methods=['GET'])
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from route.admin.admin_middleware import admin_required

from user import get_user_by_id_or_email

# GET /admin/user?user_id=123 HTTP/1.1
# Host: yourdomain.com
# Authorization: Bearer <JWT_TOKEN>


@admin_required
def get_user_details():
    # Get the current admin user details from the JWT
    current_user = get_jwt_identity()  # Admin info (this is already authenticated)

    # Get user data to be fetched from the query parameters
    user_id = request.args.get('user_id')  # The ID of the user to fetch
    email = request.args.get('email')      # The email of the user to fetch
    # Ensure at least one identifier is provided (user_id or email)
    if not user_id and not email:
        return jsonify({"error": "Either user_id or email must be provided to identify the user."}), 400

    # Fetch user details from the database
    user = get_user_by_id_or_email(user_id=user_id, email=email)

    if not user:
        return jsonify({"error": "User not found."}), 404

    # Return user details
    return jsonify({
        "user_id": user[0],
        "email": user[1],
        "name": user[2],
        "role": user[3],
        "created_on": user[4],
        "is_active": user[5]
    }), 200


