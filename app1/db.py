# db.py
import psycopg2
from psycopg2 import pool
from config import Config

# Initialize the connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,  # Minimum number of connections in the pool
    maxconn=10,  # Maximum number of connections in the pool
    dsn=Config.DATABASE_URL
)

def get_connection():
    """
    Get a connection from the pool.
    """
    if connection_pool:
        print("start")
        return connection_pool.getconn()

def release_connection(conn):
    """
    Release a connection back to the pool.
    """
    if connection_pool and conn:
        connection_pool.putconn(conn)
        print("done")

def close_all_connections():
    """
    Close all connections in the pool. Use when shutting down the app.
    """
    if connection_pool:
        connection_pool.closeall()
        print("close")
