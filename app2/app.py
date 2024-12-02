from flask import Flask
from config import Config, mail
from database import setup_database
from route.disable_2fa import disable_auth
from route.enable_2fa import enable_auth
from route.user_register import user_register
from route.admin_register import admin_register
from route.sign_in import sign_in_bp
from route.get_details import fetch
from route.activate_data import activate_data
from route.blacklist import blacklist
from route.resend_verification import resend_mail
from route.reset_password import reset_password
from route.request_reset_password import request_pwd_reset
from route.change_password import change_password

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config.from_object(Config)
app.json.sort_keys = False

# Initialize Flask-Mail with the app
mail.init_app(app)
setup_database()

# Register blueprints
app.register_blueprint(blacklist)
app.register_blueprint(change_password)
app.register_blueprint(fetch)
app.register_blueprint(request_pwd_reset)
app.register_blueprint(resend_mail)
app.register_blueprint(reset_password)
app.register_blueprint(sign_in_bp)
app.register_blueprint(user_register)
app.register_blueprint(admin_register)
app.register_blueprint(activate_data)
app.register_blueprint(enable_auth)
app.register_blueprint(disable_auth)

if __name__ == "__main__":
    app.run(debug=True)

# request.args.get("code")

