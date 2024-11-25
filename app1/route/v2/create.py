from flask import Blueprint, request, jsonify
from validate import validate_product_data  # Import validation function
from db import get_connection, release_connection  # Import connection pool functions

create = Blueprint('create', __name__)

@create.route('/product', methods=['POST'])
def add_product():
    data = request.get_json()
    is_valid, error_message = validate_product_data(data)
    if not is_valid:
        return jsonify({'message': error_message}), 400
    try:
        
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO products (name, category, tags, mrp, sale_price, image, description, slug) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (data['name'], data['category'], data['tags'], float(data['mrp']), float(data['sale_price']), data['image'], data['description'], data['slug'])
            )
        conn.commit()
        return jsonify({'message': 'product created'}), 201
    except Exception as e:
        return jsonify({'message': f'error adding product: {e}'}), 500
    finally:
        release_connection(conn)  # Release the connection back to the pool

# paramaterized query