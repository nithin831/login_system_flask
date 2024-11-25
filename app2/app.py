from flask import Flask, request
from route.user_register import register_user
from route.sign_in import login
from route.get_user import get_user_details
from route.verify import verify_user
from config import Config, mail
from database import setup_database
from route.blacklist_user import blacklist_user_endpoint
from route.resend_verification import resend_activation

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config.from_object(Config)

# Initialize Flask-Mail with the app
mail.init_app(app)
setup_database()

@app.route('/user/register', methods=['POST'])
def user_register_route():
    return register_user(data=request.get_json(), role="user")

@app.route('/admin/register', methods=['POST'])
def admin_register_route():
    return register_user(data=request.get_json(), role="admin")

@app.route('/sign_in', methods=['POST'])
def signin_route():
    return login(data=request.get_json())

@app.route('/fetch', methods=['GET'])
def get_user_route():
    return get_user_details(token=request.headers.get("Authorization"))

@app.route('/blacklist/email', methods=['PUT'])
def blacklist_user():
    return blacklist_user_endpoint(data=request.get_json())

@app.route('/verify', methods=['GET'])
def verify():
    return verify_user(token = request.args.get('token'))

@app.route('/resend-activation', methods=['POST'])
def resend_mail():
    return resend_activation(data=request.get_json())

if __name__ == "__main__":
    app.run(debug=True)

