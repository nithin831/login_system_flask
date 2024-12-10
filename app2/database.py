import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import Config
import logging
import os
from psycopg2 import pool
from contextlib import contextmanager
from psycopg2.extras import RealDictCursor

# connection_pool = None

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

# def setup_database():
#     """Ensure the target database and tables exist, then set up the connection pool."""
#     global connection_pool
#
#     # Ensure the database exists
#     create_database_if_not_exists()
#
#     try:
#         # Now initialize the connection pool for the target database
#         print("Initializing connection pool...")
#         connection_pool = psycopg2.pool.SimpleConnectionPool(
#             minconn=1,
#             maxconn=10,
#             dsn=Config.DATABASE_URL
#         )
#         if connection_pool:
#             print("Connection pool created successfully.")
#
#         # Set up tables in the target database
#         conn = get_connection()
#         conn.autocommit = True
#         try:
#             with conn.cursor() as cursor:
#                 cursor.execute("DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole') THEN CREATE TYPE userrole AS ENUM ('admin', 'user'); END IF; END $$;")
#
#                 cursor.execute(
#                     """
#                     CREATE TABLE IF NOT EXISTS user_table (
#                         id SERIAL PRIMARY KEY,
#                         email VARCHAR(255) UNIQUE NOT NULL,
#                         password BYTEA NOT NULL,
#                         name VARCHAR(100) NOT NULL,
#                         role userrole NOT NULL,  -- Using ENUM type for role
#                         created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                         secret_key VARCHAR(255) NULL,
#                         is_active BOOLEAN DEFAULT FALSE,
#                         blacklist BOOLEAN DEFAULT FALSE,
#                         is_2fa BOOLEAN DEFAULT FALSE
#                     );
#                     """
#                 )
#                 print("Users table created or already exists.")
#         finally:
#             release_connection(conn)
#     except Exception as e:
#         print(f"Error during setup_database: {e}")
#
# def get_connection():
#     """Get a connection from the pool."""
#     if connection_pool:
#         return connection_pool.getconn()
#     raise Exception("Connection pool is not initialized.")
#
# def release_connection(conn):
#     """Release a connection back to the pool."""
#     if connection_pool and conn:
#         connection_pool.putconn(conn)
#
# def close_all_connections():
#     """Close all connections in the pool."""
#     if connection_pool:
#         connection_pool.closeall()




class PGConnectionPool:
    def __init__(self, dsn: str, min_conn: int = 1, max_conn: int = 5):
        """
        Creates A Simple Connection Pool Using DB Credentials

        Example Usage:
        with conn_pool.get_cursor(cursor_type=RealDictCursor) as cur:
            cur.execute(query)
            results = cur.fetchall()
            print(results)```

        """
        print("nk")
        self.conn_pool = pool.ThreadedConnectionPool(
            minconn=min_conn, maxconn=max_conn, dsn=dsn
        )

    @contextmanager
    def get_cursor(self, cursor_type=RealDictCursor, debug=False):
        """
        Get A Cursor From Connection Pool And Putback the Connection After use
        :param cursor_type: RealDictCursor (Default)
        :param debug: False (default) -- To Debug The Exact SQL query
        """
        conn = self.conn_pool.getconn()
        try:
            print("Connection checked out")
            cur = conn.cursor(cursor_factory=cursor_type)
            yield cur
            if debug:
                print(f"Executed Query: {cur.query.decode()}")
        except Exception as e:
            print(f"Rolling back due to exception: {e}")
            conn.rollback()
            raise
        finally:
            self.conn_pool.putconn(conn)
            # print("Connection checked back in")

    def close_all(self):
        """Close all connections in the pool."""
        self.conn_pool.closeall()


conn_pool = PGConnectionPool(dsn=Config.DATABASE_URL)
# conn_pool = PGConnectionPool(host=os.environ.get('POSTGRES_HOST'),
#                              db_name=os.environ.get('POSTGRES_DATABASE'),
#                              username=os.environ.get('POSTGRES_USER'),
#                              password=os.environ.get('POSTGRES_PASSWORD'),
#                              port=int(os.environ.get('POSTGRES_PORT', 5432)))