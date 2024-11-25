
from database import get_connection, release_connection
# from utils.redis_utils import redis_client

def blacklist_user(email):
    """
    Blacklists the user by setting `blacklist` to true in PostgreSQL.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Update is_active to FALSE in PostgreSQL
            cur.execute(
                """
                UPDATE user_table
                SET blacklist = TRUE
                WHERE email = %s
                RETURNING id;
                """, (email,)
            )
            user_id = cur.fetchone()
            if user_id:
                conn.commit()
                user_id = user_id[0]  # Extract user ID from the result

                # Remove the JWT from Redis using the Redis key for this user
                # redis_key = f"jwt:{user_id}"
                # redis_client.delete(redis_key)
                return {"message": f"User with email {email} has been blacklisted."}
            else:
                return {"error": "User not found."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        release_connection(conn)
