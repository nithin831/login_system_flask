from flask import Flask
from config import Config, mail
from route.account.account import account
from route.admin.admin import admin
from route.social_auth.facebook import auth_facebook
from route.social_auth.github import auth_github
from route.social_auth.google import auth_google
from route.social_auth.linkedin import auth_linkedin
from route.social_auth.login_with_out_password import passwordless

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config.from_object(Config)
app.json.sort_keys = False

# Initialize Flask-Mail with the app
mail.init_app(app)

# Register blueprints
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(auth_github, url_prefix='/github')
app.register_blueprint(auth_google, url_prefix='/google')
app.register_blueprint(auth_linkedin, url_prefix='/linkedin')
app.register_blueprint(auth_facebook, url_prefix='/facebook')
app.register_blueprint(passwordless, url_prefix='/passwordless')


if __name__ == "__main__":
    app.run(debug=True)


