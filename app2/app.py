from flask import Flask
from config import Config, mail
from route.account.account import account
from route.admin.admin import admin
from route.social_auth.github import auth
from route.social_auth.google import auth_google

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config.from_object(Config)
app.json.sort_keys = False

# Initialize Flask-Mail with the app
mail.init_app(app)

# Register blueprints
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(auth_google, url_prefix='/auth_google')

if __name__ == "__main__":
    app.run(debug=True)

# request.args.get("code")

