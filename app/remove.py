from flask import Blueprint, jsonify, make_response
from db import db
from models import Product

delete = Blueprint('remove', __name__)

@delete.route('/product/<int:id>/delete', methods=['DELETE'])
def remove_product(id):
    try:
        product = Product.query.get(id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return make_response(jsonify({'message': 'product deleted'}), 200)
        return make_response(jsonify({'message': 'product not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting product'}), 500)
    