from flask import  Flask
from login_rate import  login_blueprint
from redis_conn import cachee

app = Flask(__name__)

app.register_blueprint(login_blueprint)
app.register_blueprint(cachee,url_prefix='/cache')

if __name__ == "__main__":
    app.run(debug=True)