from flask import Blueprint, request, request, jsonify, make_response
from db import db
from models import Product

update = Blueprint('update', __name__)

@update.route('/product/<int:id>', methods=['PUT'])
def modify_product(id):
    try:
        product = Product.query.get(id)
        if not product:
            return make_response(jsonify({'message': 'product not found'}), 404)
         
        data = request.get_json()
        product.name = data['name']
        product.category = data['category']
        product.tags = data['tags']
        product.mrp = float(data['mrp'])
        product.sale_price = float(data['sale_price'])
        product.image = data['image']
        product.description = data['description']
        product.slug = data['slug']
        db.session.commit()
        return make_response(jsonify({'message': 'product updated'}), 200)
    except Exception as e:
        # raise e
        return make_response(jsonify({'message': f'error updating product {e}'}), 500)
    
