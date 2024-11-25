from flask import Flask, jsonify, make_response
from config import Config
from db import db
from create import create
from update import update
from remove import delete
from view import view
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
app.secret_key = "nithin"  # Set your secret key for session management

app.config.from_object(Config)

db.init_app(app)

# Function to set up the database
def setup_database():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database created at '{engine.url}'.")
    else:
        print(f"Database at '{engine.url}' already exists.")
    
    with app.app_context():
        db.create_all()  # Create all tables
        
setup_database()

# Register blueprints
app.register_blueprint(create)
app.register_blueprint(update)
app.register_blueprint(delete)
app.register_blueprint(view)

@app.route('/')
def home():
    return make_response(jsonify({'message': 'working'}), 200)

if __name__ == "__main__":
    app.run(debug=True)
