
from functools import wraps
import redis
from flask import jsonify, Blueprint

cachee=Blueprint("cache",__name__)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def cache(ttl: int):
    def decorator(func):
        @wraps(func)  # Preserve the original function's metadata
        def wrapper(*args, **kwargs):
            key = f"cache:{func.__name__}:{args}:{kwargs}"  # Unique cache key
            if redis_client.exists(key):
                return jsonify({"cached_result": redis_client.get(key)})  # Return cached value
            result = func(*args, **kwargs)  # Call the original function
            redis_client.set(key, result, ex=ttl)  # Cache the result with TTL
            return result
        return wrapper
    return decorator

@cachee.route('/cache', methods=["GET"])
@cache(ttl=300)  # Cache results for 5 minutes
def expensive_operation():
    import time
    time.sleep(2)  # Simulate an expensive operation
    return "Expensive operation result"