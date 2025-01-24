from flask import request, jsonify, Blueprint
from rate_limit_login import rate_limit
from validate_request import validate_request


login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=["POST"])
@rate_limit(limit=5, window=60)
@validate_request(["username", "password"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    if username == "admin" and password == "password123":
        return jsonify({"message": "Login successful!"})
    return jsonify({"error": "Invalid credentials"}), 401