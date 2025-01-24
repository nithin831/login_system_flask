# # import pickle
# # import time
# # from functools import wraps
# #
# # import redis
# #
# #
# # class RedisCache:
# #     def _init_(self, redis_client: redis.Redis, default_expiration_time=None):
# #         if not isinstance(redis_client, redis.Redis):
# #             raise ValueError("Invalid Redis instance")
# #         self.redis_instance = redis_client
# #         self.default_expiration_time = default_expiration_time
# #
# #     def get(self, key):
# #         result = self.redis_instance.get(key)
# #         if result is not None:
# #             result = pickle.loads(result)
# #         return result
# #
# #     def set(self, key, value, expiration_time=None):
# #         if expiration_time:
# #             self.redis_instance.set(key, pickle.dumps(value), ex=expiration_time)
# #         else:
# #             self.redis_instance.set(key, pickle.dumps(value))
# #
# #     def ttl(self, key):
# #         return self.redis_instance.ttl(key)
# #
# #     def delete(self, key):
# #         self.redis_instance.delete(key)
# #
# #     def cache_result(self, ttl=None, cache_key=None):
# #
# #         def decorator(func):
# #             @wraps(func)
# #             def wrapper(*args, cache_key=None, **kwargs):
# #                 if cache_key:
# #                     if callable(cache_key):
# #                         _cache_key = cache_key(*args, **kwargs)
# #                     else:
# #                         _cache_key = cache_key
# #                 else:
# #                     cache_key = f"{func.module}:{func.name}:{args}:{kwargs}" if kwargs else f"{func.module}:{func.name_}:{args}"
# #                 result = self.get(_cache_key)
# #                 if result is not None:
# #                     return result
# #                 result = func(*args, **kwargs)
# #                 self.set(_cache_key, result, expiration_time=ttl or self.default_expiration_time)
# #                 return result
# #
# #             return wrapper
# #
# #         return decorator
# #
# #
# # cache = RedisCache(redis_client=redis.Redis.from_url("redis://localhost:6379/0"))
# #
# # @cache.cache_result()
# # def get_state_analytics(state_name):
# #     time.sleep(3)
# #     return {"state_name": state_name, "total": 200000}
# #
# #
# # t1 = time.time()
# # print(get_state_analytics("kar"))
# # print(time.time() - t1)
# #
# #
#
#
#
# # import pickle
# # import time
# # from functools import wraps
# #
# # import redis
# #
# #
# # class RedisCache:
# #     def __init__(self, redis_client: redis.Redis, default_expiration_time=None):
# #         if not isinstance(redis_client, redis.Redis):
# #             raise ValueError("Invalid Redis instance")
# #         self.redis_instance = redis_client
# #         self.default_expiration_time = default_expiration_time
# #
# #     def get(self, key):
# #         result = self.redis_instance.get(key)
# #         if result is not None:
# #             result = pickle.loads(result)
# #         return result
# #
# #     def set(self, key, value, expiration_time=None):
# #         if expiration_time:
# #             self.redis_instance.set(key, pickle.dumps(value), ex=expiration_time)
# #         else:
# #             self.redis_instance.set(key, pickle.dumps(value))
# #
# #     def ttl(self, key):
# #         return self.redis_instance.ttl(key)
# #
# #     def delete(self, key):
# #         self.redis_instance.delete(key)
# #
# #     def invalidate(self, cache_key):
# #         """Manually invalidate a cache entry."""
# #         self.delete(cache_key)
# #
# #     def cache_result(self, ttl=None, cache_key=None, invalidate_on_change=False):
# #         """Cache decorator with the option to invalidate cache explicitly."""
# #         def decorator(func):
# #             @wraps(func)
# #             def wrapper(*args, cache_key=None, invalidate_cache=False, **kwargs):
# #                 if cache_key:
# #                     if callable(cache_key):
# #                         _cache_key = cache_key(*args, **kwargs)
# #                     else:
# #                         _cache_key = cache_key
# #                 else:
# #                     _cache_key = f"{func.__module__}:{func.__name__}:{args}:{kwargs}" if kwargs else f"{func.__module__}:{func.__name__}:{args}"
# #
# #                 # Invalidate cache if requested
# #                 if invalidate_cache:
# #                     self.invalidate(_cache_key)
# #                     return func(*args, **kwargs)
# #
# #                 result = self.get(_cache_key)
# #                 if result is not None:
# #                     return result
# #
# #                 # Cache miss, call the function and cache the result
# #                 result = func(*args, **kwargs)
# #                 self.set(_cache_key, result, expiration_time=ttl or self.default_expiration_time)
# #                 return result
# #
# #             return wrapper
# #
# #         return decorator
# #
# #
# # cache = RedisCache(redis_client=redis.Redis.from_url("redis://localhost:6379/0"))
# #
# #
# # @cache.cache_result()
# # def get_state_analytics(state_name):
# #     time.sleep(3)  # Simulating a time-consuming operation
# #     return {"state_name": state_name, "total": 200000}
# #
# #
# # # Usage example
# #
# # t1 = time.time()
# # print(get_state_analytics("kar"))
# # print(time.time() - t1)
# #
# # # Invalidate the cache manually
# # cache.invalidate(f"{get_state_analytics.__module__}:{get_state_analytics.__name__}:('kar',)")
# #
# # t2 = time.time()
# # print(get_state_analytics("kar"))
# # print(time.time() - t2)
# J
#
# import pickle
# import time
# import logging
# from functools import wraps
# import redis
#
#
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
#
# class RedisCache:
#     def __init__(self, redis_client: redis.Redis, default_expiration_time=None):
#         if not isinstance(redis_client, redis.Redis):
#             raise ValueError("Invalid Redis instance")
#         self.redis_instance = redis_client
#         self.default_expiration_time = default_expiration_time
#
#     def get(self, key):
#         try:
#             result = self.redis_instance.get(key)
#             if result is not None:
#                 result = pickle.loads(result)
#             return result
#         except redis.RedisError as e:
#             logger.error(f"Error fetching from Redis: {e}")
#             return None
#
#     def set(self, key, value, expiration_time=None):
#         try:
#             serialized_value = pickle.dumps(value)
#             expiration_time = expiration_time or self.default_expiration_time
#             self.redis_instance.set(key, serialized_value, ex=expiration_time)
#         except redis.RedisError as e:
#             logger.error(f"Error setting value in Redis: {e}")
#
#     def ttl(self, key):
#         try:
#             return self.redis_instance.ttl(key)
#         except redis.RedisError as e:
#             logger.error(f"Error getting TTL for key {key}: {e}")
#             return None
#
#     def delete(self, key):
#         try:
#             self.redis_instance.delete(key)
#         except redis.RedisError as e:
#             logger.error(f"Error deleting key {key} from Redis: {e}")
#
#     def invalidate(self, cache_key):
#         """Manually invalidate a cache entry."""
#         self.delete(cache_key)
#
#     def cache_result(self, ttl=None, cache_key=None):
#         """Cache decorator with the option to invalidate cache explicitly."""
#         def decorator(func):
#             @wraps(func)
#             def wrapper(*args, cache_key=None, invalidate_cache=False, **kwargs):
#                 # Cache Key Generation
#                 if cache_key:
#                     if callable(cache_key):
#                         _cache_key = cache_key(*args, **kwargs)
#                     else:
#                         _cache_key = cache_key
#                 else:
#                     _cache_key = f"{func.__module__}:{func.__name__}:{args}:{kwargs}"
#
#                 # Invalidate cache if requested
#                 if invalidate_cache:
#                     logger.info(f"Invalidating cache for key: {_cache_key}")
#                     self.invalidate(_cache_key)
#                     return func(*args, **kwargs)
#
#                 # Cache hit
#                 result = self.get(_cache_key)
#                 if result is not None:
#                     logger.info(f"Cache hit for key: {_cache_key}")
#                     return result
#
#                 # Cache miss, call the function and cache the result
#                 logger.info(f"Cache miss for key: {_cache_key}, calling the function")
#                 result = func(*args, **kwargs)
#                 self.set(_cache_key, result, expiration_time=ttl or self.default_expiration_time)
#                 return result
#
#             return wrapper
#
#         return decorator
#
#
# # Redis cache initialization
# cache = RedisCache(redis_client=redis.Redis.from_url("redis://localhost:6379/0"))
#
#
# @cache.cache_result()
# def get_state_analytics(state_name):
#     time.sleep(3)  # Simulate a time-consuming operation
#     return {"state_name": state_name, "total": 200000}
#
#
# # Example usage
# if __name__ == "__main__":
#     t1 = time.time()
#     print(get_state_analytics("kar"))
#     print(f"Time taken: {time.time() - t1:.2f} seconds")
#
#     # Invalidate the cache manually
#     cache.invalidate(f"{get_state_analytics.__module__}:{get_state_analytics.__name__}:('kar',)")
#
#     t2 = time.time()
#     print(get_state_analytics("kar"))
#     print(f"Time taken: {time.time() - t2:.2f} seconds")
