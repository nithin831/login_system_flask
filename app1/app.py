import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask import Flask, jsonify, make_response
from config import Config

from route.v2.create import create
from route.v2.update import update
from route.v2.remove import delete
from route.v2.view import view

from db import close_all_connections  # Import the function to close all connections

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

def create_database_if_not_exists():
    """Connect to the default database and create the specified database if it doesn't exist."""
    default_connection = psycopg2.connect(app.config['DATABASE_URL'].rsplit('/', 1)[0] + "/postgres")  # Connect to default `postgres` database
    default_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    db_name = app.config['DATABASE_URL'].rsplit('/', 1)[1]  # Extract database name from URL
    print(db_name)

    with default_connection.cursor() as cursor:
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created.")
        else:
            print(f"Database '{db_name}' already exists.")
    default_connection.close()

def setup_database():
    """Connect to the specific database and set up tables if they don't exist."""
    create_database_if_not_exists()  # Ensure database exists

    conn = psycopg2.connect(app.config['DATABASE_URL'])
    conn.autocommit = True
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                tags VARCHAR(100),
                mrp INTEGER NOT NULL,
                sale_price INTEGER NOT NULL,
                image VARCHAR(200),
                description TEXT,
                slug VARCHAR(100) NOT NULL
            )
            """
        )
    conn.close()

setup_database()

@app.teardown_appcontext
def shutdown_session(exception=None):
    close_all_connections()  # Close the connection pool when the app shuts down

# Register blueprints
app.register_blueprint(create, url_prefix='/v2')
app.register_blueprint(update, url_prefix='/v2')
app.register_blueprint(delete, url_prefix='/v2')
app.register_blueprint(view, url_prefix='/v2')

@app.route('/')
def home():
    return make_response(jsonify({'message': 'working1'}), 200)

if __name__ == "__main__":
    app.run(debug=True)
