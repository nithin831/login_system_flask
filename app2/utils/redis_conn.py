import json
import os
from functools import wraps
import redis
from flask import request, jsonify, Response

from utils.jwt_utils import decode_jwt_token

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
redis_client = redis.StrictRedis.from_url(redis_url)

def cache(ttl: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Assuming the JWT token is passed as a header (or any way you pass it)
            token = request.headers.get('Authorization')

            if token:
                # Remove the "Bearer " part
                token = token.split(" ")[1] if token.startswith("Bearer ") else token
                print(token)
            else:
                return jsonify({"error": "Authorization header is missing."}), 400
            payload = decode_jwt_token(token)
            print("this is decoded toekn:",payload)# Decode JWT to get user email
            if not payload["email"]:
                return jsonify({"error": "Invalid or expired token."}), 401
            # Unique cache key based on function name, user email, and query arguments
            key = f"cache:{func.__name__}:{payload}:{str(args)}:{str(kwargs)}"
            # Check if the result is cached in Redis
            cached_result = redis_client.get(key)
            print("cache result:",cached_result)
            if cached_result:
                print(f"Cache hit: {key}")
                return jsonify({"cached_result": json.loads(cached_result)})
            # Cache miss: Compute the result by querying the database
            print(f"Cache miss: {key}")
            result = func(*args, **kwargs, email=payload)  # Pass email to the function
            # Convert result to JSON if it's not a Response object
            if isinstance(result, Response):  # If it's a Response (like from jsonify)
                result_data = result.get_data(as_text=True)  # Get the response body as string
            else:
                result_data = json.dumps(result)  # Store the result as a JSON string
            # Cache the result with TTL (Time to Live)
            print("data from cache",redis_client.setex(key, ttl, result_data))
            if isinstance(result, Response):
                return result  # If it's a Response, return it as is
            else:
                return jsonify(result)
        return wrapper
    return decorator