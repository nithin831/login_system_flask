import bcrypt
from database import conn_pool

def create_user(email, password, name, role, is_active):
    with conn_pool.get_cursor() as cur:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur.execute("""
            INSERT INTO user_table (email, password, name, role, created_on, is_active, blacklist)
            VALUES (%(email)s, %(password)s, %(name)s, %(role)s, NOW(), %(is_active)s, FALSE)
        """, {
            'email': email,
            'password': hashed_password,
            'name': name,
            'role': role,
            'is_active': is_active
        })
        cur.connection.commit()

def fetch_sign_in(email):
    with conn_pool.get_cursor() as cur:
        cur.execute("SELECT password, role, is_active, name, blacklist, is_2fa FROM user_table WHERE email = %s", (email,))
        return cur.fetchone()

def check_user_exist(email):
    with conn_pool.get_cursor() as cur:
        # Check if email already exists in the database
        cur.execute("SELECT is_active, blacklist FROM user_table WHERE email = %s", (email,))
        return cur.fetchone()

# update user
def update_user(email, password, name, role, is_active):
    with conn_pool.get_cursor() as cur:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur.execute("""
            UPDATE user_table
            SET password = %(password)s,
                name = %(name)s,
                role = %(role)s,
                created_on = NOW(),
                is_active = %(is_active)s,
                blacklist = FALSE
            WHERE email = %(email)s
        """, {
            'email': email,
            'password': hashed_password,
            'name': name,
            'role': role,
            'is_active': is_active
        })
        cur.connection.commit()

def update_new_password(new_password, email):
    with conn_pool.get_cursor() as cur:
        # Hash the new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        cur.execute("UPDATE user_table SET password = %s WHERE email = %s", (hashed_password, email))
        cur.connection.commit()

def activate_user(email):
    with conn_pool.get_cursor() as cur:
        cur.execute("UPDATE user_table SET is_active = TRUE WHERE email = %s", (email,))
        cur.connection.commit()

def blacklist_mail(email):
    with conn_pool.get_cursor() as cur:
        cur.execute(
            """
            UPDATE user_table
            SET blacklist = TRUE
            WHERE email = %s
            RETURNING id;
            """, (email,)
        )
        cur.connection.commit()

def fetch_password(email):
    with conn_pool.get_cursor() as cur:
        # Fetch user details
        cur.execute("SELECT password FROM user_table WHERE email = %s", (email,))
        return cur.fetchone()

def update_secret_key(secret_key, email):
    with conn_pool.get_cursor() as cur:
        cur.execute("UPDATE user_table SET secret_key = %s WHERE email = %s", (secret_key, email))
        cur.connection.commit()

def fetch_secret_key(email):
    with conn_pool.get_cursor() as cur:
        cur.execute("SELECT secret_key FROM user_table WHERE email = %s", (email,))
        return cur.fetchone()

def update_2fa(is_2fa, email):
    with conn_pool.get_cursor() as cur:
        cur.execute("UPDATE user_table SET is_2fa = %s WHERE email = %s", (is_2fa, email))
        cur.connection.commit()

def fetch_users_from_db(page, per_page, email=None, name=None, role=None, is_active=None, search=None):
    query = "SELECT id, email, name, role, created_on, is_active, blacklist FROM user_table"
    count_query = "SELECT COUNT(*) FROM user_table"
    filters = []
    params = []
    # Apply filters based on the provided parameters
    if email:
        filters.append("email = %s")
        params.append(email)
    if name:
        filters.append("name ILIKE %s")
        params.append(f"%{name}%")
    if role:
        filters.append("role = %s")
        params.append(role)
    if is_active:
        filters.append("is_active = %s")
        params.append(is_active)
    if search:
        filters.append("(email ILIKE %s OR name ILIKE %s)")
        params.extend([f"%{search}%", f"%{search}%"])
    if filters:
        filter_clause = " WHERE " + " AND ".join(filters)
        query += filter_clause
        count_query += filter_clause
    # Execute the count query
    with conn_pool.get_cursor() as cur:
        cur.execute(count_query, tuple(params))
        total_count = cur.fetchone()
    # Add pagination
    query += " ORDER BY created_on DESC LIMIT %s OFFSET %s"
    params.extend([per_page, (page - 1) * per_page])
    # Execute the main query to fetch users
    with conn_pool.get_cursor() as cur:
        cur.execute(query, tuple(params))
        users = cur.fetchall()
    return users, total_count

def update_user_details(email, update_fields):
    if not update_fields:
        raise ValueError("No fields provided to update.")
    set_clauses = []
    params = []
    # Dynamically construct the SET clause for the update query
    for field, value in update_fields.items():
        if field == "password":
            # Hash the password before updating
            value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
        set_clauses.append(f"{field} = %s")
        params.append(value)
    # Add email as the condition
    params.append(email)
    # Build the SQL query
    query = f"""
        UPDATE user_table
        SET {", ".join(set_clauses)}
        WHERE email = %s
    """
    # Execute the query
    with conn_pool.get_cursor() as cur:
        cur.execute(query, tuple(params))
        cur.connection.commit()



