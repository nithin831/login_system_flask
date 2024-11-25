from flask import Blueprint, request, jsonify
from db import get_connection, release_connection  # Import connection pool functions
from validate import validate_product_data  # Import validation function

update = Blueprint('update', __name__)

@update.route('/product/<int:id>', methods=['PUT'])
def modify_product(id):
    data = request.get_json()
    is_valid, error_message = validate_product_data(data)
    if not is_valid:
        return jsonify({'message': error_message}), 400
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE products SET name = %s, category = %s, tags = %s, mrp = %s, sale_price = %s, image = %s, description = %s, slug = %s WHERE id = %s",
                (data['name'], data['category'], data['tags'], float(data['mrp']), float(data['sale_price']), data['image'], data['description'], data['slug'], id)
            )
        conn.commit()
        return jsonify({'message': 'product updated'}), 200
    except Exception as e:
        return jsonify({'message': f'error updating product: {e}'}), 500
    finally:
        release_connection(conn)  # Release the connection back to the pool
