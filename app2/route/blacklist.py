from flask import jsonify, Blueprint, request
from user import *
from utils.auth_check import is_admin
from validate import *

blacklist = Blueprint('blacklist', __name__)
@blacklist.put('/blacklist/email')
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