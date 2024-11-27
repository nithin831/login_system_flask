import psycopg2
from psycopg2 import pool
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import Config

connection_pool = None

def create_database_if_not_exists():
    """Connect to the default database and create the specified database if it doesn't exist."""
    # Connect to the default `postgres` database
    default_conn_url = Config.DATABASE_URL.rsplit('/', 1)[0] + "/postgres"
    default_connection = psycopg2.connect(default_conn_url)
    default_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Extract the target database name from the URL
    db_name = Config.DATABASE_URL.rsplit('/', 1)[1]
    
    try:
        with default_connection.cursor() as cursor:
            # Check if the target database exists
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            if not cursor.fetchone():
                # Create the target database if it doesn't exist
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"Database '{db_name}' created.")
            else:
                print(f"Database '{db_name}' already exists.")
    finally:
        default_connection.close()

def setup_database():
    """Ensure the target database and tables exist, then set up the connection pool."""
    global connection_pool
    
    # Ensure the database exists
    create_database_if_not_exists()

    try:
        # Now initialize the connection pool for the target database
        print("Initializing connection pool...")
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=Config.DATABASE_URL
        )
        if connection_pool:
            print("Connection pool created successfully.")
        
        # Set up tables in the target database
        conn = get_connection()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute("DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole') THEN CREATE TYPE userrole AS ENUM ('admin', 'user'); END IF; END $$;")

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS user_table (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password BYTEA NOT NULL,
                        name VARCHAR(100) NOT NULL,
                        role userrole NOT NULL,  -- Using ENUM type for role
                        created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        secret_key VARCHAR(255) NULL,
                        is_active BOOLEAN DEFAULT FALSE,
                        blacklist BOOLEAN DEFAULT FALSE
                    );
                    """
                )
                print("Users table created or already exists.")
        finally:
            release_connection(conn)
    except Exception as e:
        print(f"Error during setup_database: {e}")
        
def get_connection():
    """Get a connection from the pool."""
    if connection_pool:
        return connection_pool.getconn()
    raise Exception("Connection pool is not initialized.")

def release_connection(conn):
    """Release a connection back to the pool."""
    if connection_pool and conn:
        connection_pool.putconn(conn)

def close_all_connections():
    """Close all connections in the pool."""
    if connection_pool:
        connection_pool.closeall()
