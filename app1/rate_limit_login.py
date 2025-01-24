from flask import Flask, request, jsonify
from redis_conn import redis_client
from functools import wraps

def rate_limit(limit: int, window: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_ip = request.remote_addr
            key = f"login_rate:{user_ip}"

            current_count = redis_client.get(key)
            if current_count:
                current_count = int(current_count)
                if current_count >= limit:
                    retry_after = redis_client.ttl(key)
                    return jsonify({"error": "Rate limit exceeded", "retry_after": retry_after}), 429
                else:
                    redis_client.incr(key)
            else:
                redis_client.set(key, 1, ex=window)

            return func(*args, **kwargs)
        return wrapper

    return decorator

