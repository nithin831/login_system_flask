
# import redis
# from config import Config

# # Initialize Redis client
# redis_pool = redis.ConnectionPool(
#     host=Config.REDIS_HOST,
#     port=Config.REDIS_PORT,
#     db=0,
#     decode_responses=True,
#     max_connections=10  # Maximum number of connections in the pool
# )

# # Create Redis client using the connection pool
# redis_client = redis.Redis(connection_pool=redis_pool)

# def test_redis_connection():
#     """Check if Redis is connected."""
#     try:
#         # Ping Redis to confirm connection
#         response = redis_client.ping()
#         if response:
#             print("Connected to Redis successfully.")
#             return True
#     except redis.ConnectionError:
#         print("Failed to connect to Redis.")
#         raise Exception

