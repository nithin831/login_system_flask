# import redis
# import psycopg2
# from psycopg2 import pool
# from functools import wraps
# import json
# import jwt
# from flask import Flask, request, jsonify, Response
#
# # Redis connection
# redis_client = redis.StrictRedis(
#     host="localhost",  # Redis server host
#     port=6379,         # Redis server port
#     db=0,              # Redis database index
#     decode_responses=True  # Automatically decode responses to strings
# )
#
# # PostgreSQL connection pooling
# db_pool = psycopg2.pool.SimpleConnectionPool(
#     1, 20,  # Min and max connections in the pool
#     host="127.0.0.1",
#     port=5432,
#     database="crudPsychopg2Db",  # Replace with your database name
#     user="postgres",  # Replace with your PostgreSQL username
#     password="password"  # Replace with your PostgreSQL password
# )
#
# # JWT secret key for decoding (replace with your actual secret key)
# SECRET_KEY = "your_secret_key"
#
#
# def decode_jwt_token(token):
#     """
#     Decodes the JWT token to extract the user email.
#     Assumes the token contains an 'email' or other relevant data.
#     """
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return payload.get("email")  # Return the email from the payload
#     except jwt.ExpiredSignatureError:
#         return None
#     except jwt.InvalidTokenError:
#         return None
#
#
# def fetch_data_from_db(query, email):
#     """
#     Function to fetch user-specific data from the database using connection pooling.
#     The query uses the user's email to fetch data.
#     """
#     conn = db_pool.getconn()  # Get a connection from the pool
#     try:
#         cursor = conn.cursor()
#         # Assuming the query is parameterized to fetch data based on the user's email
#         cursor.execute(query, (email,))
#         result = cursor.fetchall()  # Fetch all results
#         return result
#     finally:
#         db_pool.putconn(conn)  # Return the connection to the pool
#
#
# def cache(ttl: int):
#     """
#     Cache decorator that first checks Redis and fetches data from the DB if not cached.
#     """
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             # Assuming the JWT token is passed as a header (or any way you pass it)
#             token = request.headers.get('Authorization')  # Extract token
#             email = decode_jwt_token(token)  # Decode JWT to get user email
#
#             if not email:
#                 return jsonify({"error": "Invalid or expired token."}), 401
#
#             # Unique cache key based on function name, user email, and query arguments
#             key = f"cache:{func.__name__}:{email}:{args}:{kwargs}"
#
#             # Check if the result is cached in Redis
#             cached_result = redis_client.get(key)
#
#             if cached_result:
#                 print(f"Cache hit: {key}")
#                 return jsonify({"cached_result": json.loads(cached_result)})
#
#             # Cache miss: Compute the result by querying the database
#             print(f"Cache miss: {key}")
#             result = func(*args, **kwargs, email=email)  # Pass email to the function
#
#             # Convert result to JSON if it's not a Response object
#             if isinstance(result, Response):  # If it's a Response (like from jsonify)
#                 result_data = result.get_data(as_text=True)  # Get the response body as string
#             else:
#                 result_data = json.dumps(result)  # Store the result as a JSON string
#
#             # Cache the result with TTL (Time to Live)
#             redis_client.setex(key, ttl, result_data)  # Cache the result for the given TTL
#             return result
#         return wrapper
#     return decorator
#
#
# # Example query function that fetches data based on user email
# @cache(ttl=3600)  # Cache for 1 hour
# def get_user_data(query, email):
#     # This function will query the database for user-specific data using the email
#     return fetch_data_from_db(query, email)
#
#
# # Example of an API endpoint to use the caching and database fetching
# app = Flask(__name__)
#
# @app.route("/user-data", methods=["GET"])
# def user_data():
#     query = "SELECT * FROM Product WHERE user_email = %s;"  # Example query that fetches data for the user based on email
#     data = get_user_data(query)  # Fetch data with caching
#     return jsonify(data)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, jsonify, request, Response
import redis
import json
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
def decode_jwt_token(token):
    if token == "valid-token":
        return "user@example.com"
    else:
        return None
def cache(ttl: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            email = decode_jwt_token(token)
            if not email:
                return jsonify({"error": "Invalid or expired token."}), 401
            key = f"cache:{func.__name__}:{email}:{str(args)}:{str(kwargs)}"
            cached_result = redis_client.get(key)
            if cached_result:
                print(f"Cache hit: {key}")
                return jsonify({"cached_result": json.loads(cached_result)})
            print(f"Cache miss: {key}")
            result = func(*args, **kwargs, email=email)
            if isinstance(result, Response):
                result_data = result.get_data(as_text=True)
            else:
                result_data = json.dumps(result)
            redis_client.setex(key, ttl, result_data)
            if isinstance(result, Response):
                return result
            else:
                return jsonify(result)
        return wrapper
    return decorator

@app.route('/account/user-data', methods=['GET'])
def user_data(*args, **kwargs):
    email = kwargs.get("email")
    user_data = {"email": email, "name": "John Doe", "age": 30}
    return jsonify(user_data)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
