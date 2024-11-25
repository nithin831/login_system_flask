import bcrypt
from database import get_connection, release_connection
from utils.jwt_utils import generate_jwt, generate_verification_token
from config import Config
# from utils.redis_utils import redis_client
from route.resend_verification import resend_activation
from utils.email_utils import send_verification_email

def create_user(email, password, name, role):  
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cur.execute("""
                INSERT INTO user_table (email, password, name, role, created_on, is_active, blacklist)
                VALUES (%(email)s, %(password)s, %(name)s, %(role)s, NOW(), FALSE, FALSE)
            """, {
                'email': email,
                'password': hashed_password,
                'name': name,
                'role': role
            })
        conn.commit()
        # Generate a verification token and send it via email
        verification_token = generate_verification_token(email)
        verification_link = f"{Config.FRONTEND_URL}/verify?token={verification_token}"
        send_verification_email(email, verification_link)
    finally:
        release_connection(conn)

def sign_in(email, password):
    """Signs in a user by verifying email and password, then returns a JWT on success."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, password, role, is_active, name, blacklist FROM user_table WHERE email = %s", (email,))
            user = cur.fetchone()
            if not user:
                return {"error": "User not found or incorrect credentials."}
            user_id, stored_password, stored_role, is_active, name, blacklist= user
            # Check if user is active
            if blacklist:
                return {"error": "User is Blacklisted. Please contact support."}
            # Validate the password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.tobytes()):
                # Generate JWT using the utility function
                token = generate_jwt(user_id, name, email, stored_role, is_active, blacklist)
                # Store JWT in Redis with expiration
                # redis_key = f"jwt:{user_id}"
                # redis_client.setex(redis_key, Config.JWT_EXPIRATION_SECONDS, token)
                return {"message": "Sign-in successful.", "token": token}
            else:
                return {"error": "User not found or incorrect credentials."}
    finally:
        release_connection(conn)
        
def check_user_exist(data):
    conn = get_connection()
    email = data.get('email')
    try:
        with conn.cursor() as cur:
            # Check if email already exists in the database
            cur.execute("SELECT is_active, blacklist FROM user_table WHERE email = %s", (email,))
            user_record = cur.fetchone()
            if user_record:
                is_active, is_blacklisted = user_record
                if is_blacklisted:
                    return {"error": "This email address is blacklisted and cannot be used for registration, please contact support."}
                if is_active:
                    return {"error": "User is already registered."}
                else:
                    resend_activation(data)
                    return {"message": "The user is already registered but not verified. A new verification link has been sent to the provided email address. Please verify your email to complete the registration process."}
        return False
    finally:
        release_connection(conn)
                

