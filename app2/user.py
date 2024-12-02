import bcrypt
from database import get_connection, release_connection
from utils.jwt_utils import generate_login_jwt_token, generate_verification_jwt_token
from config import Config
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
    finally:
        release_connection(conn)

def fetch_sign_in(email):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT password, role, is_active, name, blacklist, is_2fa FROM user_table WHERE email = %s", (email,))
            return cur.fetchone()
    finally:
        release_connection(conn)
        
def check_user_exist(data):
    conn = get_connection()
    email = data.get('email')
    try:
        with conn.cursor() as cur:
            # Check if email already exists in the database
            cur.execute("SELECT is_active, blacklist FROM user_table WHERE email = %s", (email,))
            return cur.fetchone()
    finally:
        release_connection(conn)
                
# update user 
def update_user(email, password, name, role):  
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cur.execute("""
                UPDATE user_table 
                SET password = %(password)s,
                    name = %(name)s,
                    role = %(role)s,
                    created_on = NOW(),
                    is_active = FALSE,
                    blacklist = FALSE
                WHERE email = %(email)s
            """, {
                'email': email,
                'password': hashed_password,
                'name': name,
                'role': role
            })
        conn.commit()
        # Generate a new verification token
        verification_token = generate_verification_jwt_token(email)
        verification_link = f"{Config.FRONTEND_URL}/account/activate?token={verification_token}"
        # Send the verification email
        send_verification_email(email, verification_link)
    finally:
        release_connection(conn)

def update_new_password(new_password, email):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Hash the new password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cur.execute("UPDATE user_table SET password = %s WHERE email = %s", (hashed_password, email))
        conn.commit()
    finally:
        release_connection(conn)

def activate_user(email):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE user_table SET is_active = TRUE WHERE email = %s", (email,))
        conn.commit()
    finally:
        release_connection(conn)

def blacklist_mail(email):
    """
    Blacklists the user by setting `blacklist` to true in PostgreSQL.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE user_table
                SET blacklist = TRUE
                WHERE email = %s
                RETURNING id;
                """, (email,)
            )
            conn.commit()
    finally:
        release_connection(conn)

def fetch_password(email):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Fetch user details
            cur.execute("SELECT password FROM user_table WHERE email = %s", (email,))
            return cur.fetchone()
    finally:
        release_connection(conn)

def update_secret_key(secret_key, email):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE user_table SET secret_key = %s WHERE email = %s", (secret_key, email))
        conn.commit()
    finally:
        release_connection(conn)

def fetch_secret_key(email):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT secret_key FROM user_table WHERE email = %s", (email,))
            return cur.fetchone()
    finally:
        release_connection(conn)

def update_2fa(is_2fa, email):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE user_table SET is_2fa = %s WHERE email = %s", (is_2fa, email))
        conn.commit()
    finally:
        release_connection(conn)