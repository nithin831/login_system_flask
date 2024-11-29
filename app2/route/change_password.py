from flask import jsonify, Blueprint, request
from user import change_password_logic
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
        validate_user_password(new_password)
        if new_password == current_password:
            return jsonify({"error": "New password must be different"}), 404
        response = change_password_logic(email, current_password, new_password)
        return jsonify(response),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





