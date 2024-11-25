from flask import Blueprint, request, jsonify
from db import get_connection, release_connection  # Import connection pool functions
from validate import validate_pagination  # Import the validation function


view = Blueprint('view', __name__)

@view.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 2)
    # Validate page and per_page using validate_pagination
    is_valid, error_message = validate_pagination(page, per_page)
    if not is_valid:
        return jsonify({'message': error_message}), 400
    try:
        page = int(page)
        per_page = int(per_page)
        category = request.args.get('category')
        tags = request.args.get('tags')
        search = request.args.get('search')
        
        query = "SELECT * FROM products"
        filters = []
        params = []

        if category:
            filters.append("category = %s")
            params.append(category)
        if tags:
            filters.append("tags LIKE %s")
            params.append(f"%{tags}%")
        if search:
            filters.append("name ILIKE %s")
            params.append(f"%{search}%")

        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += " LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            products = cursor.fetchall()

        products_list = [{"id": p[0], "name": p[1], "category": p[2], "tags": p[3], "mrp": p[4], "sale_price": p[5], "image": p[6], "description": p[7], "slug": p[8]} for p in products]
        
        return jsonify(products_list), 200
    except Exception as e:
        return jsonify({'message': f'error getting product: {e}'}), 500
    finally:
        release_connection(conn)  # Release the connection back to the pool