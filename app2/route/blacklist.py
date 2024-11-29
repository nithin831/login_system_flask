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
        validate_user_email(email)
        # Call the function to blacklist the user
        result = blacklist_mail(email)
        if "error" in result:
            return jsonify(result), 404  # Not found if user doesn't exist
        return jsonify(result), 200  # Success response if user was blacklisted
    except Exception as e:
        return {"error": str(e)}