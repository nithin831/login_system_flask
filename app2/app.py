from flask import Flask
from config import Config, mail
from route.account.account import account
from route.admin.admin import admin

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config.from_object(Config)
app.json.sort_keys = False

# Initialize Flask-Mail with the app
mail.init_app(app)

# Register blueprints
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(admin, url_prefix='/admin')

if __name__ == "__main__":
    app.run(debug=True)

# request.args.get("code")

