from flask import jsonify, Blueprint, request
from user import *
from utils.auth_check import is_sign_in
from validate import *

change_password = Blueprint('change_password', __name__)
@change_password.post('/change-password')
@is_sign_in
def change_password_route(email):
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    if not current_password or not new_password:
        return {"error": "Current password, and new password are required."}, 400
    try:
        response, message = validate_user_password(new_password)
        if not response:
            return jsonify({"message": message})
        if new_password == current_password:
            return jsonify({"error": "New password must be different"}), 404
        stored_password = fetch_password(email)
        # Validate the current password
        if not bcrypt.checkpw(current_password.encode('utf-8'), stored_password[0].tobytes()):
            return jsonify({"error": "Current password is incorrect."}), 401
        # Update the password in the database
        update_new_password(new_password, email)
        return jsonify({"message": "Password updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





