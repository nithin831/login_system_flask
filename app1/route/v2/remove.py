from flask import Blueprint, jsonify
from db import get_connection, release_connection  # Import connection pool functions

delete = Blueprint('remove', __name__)

@delete.route('/product/<int:id>/delete', methods=['DELETE'])
def remove_product(id):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM products WHERE id = %s", (id,))
        conn.commit()
        return jsonify({'message': 'product deleted'}), 200
    except Exception as e:
        return jsonify({'message': f'error deleting product: {e}'}), 500
    finally:
        release_connection(conn)  # Release the connection back to the pool