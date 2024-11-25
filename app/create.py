from flask import Blueprint, request, flash, request, jsonify, make_response
from db import db
from models import Product

create = Blueprint('create', __name__)

@create.route('/product', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        new_product = Product(
            name=data['name'],
            category=data['category'],
            tags=data['tags'],
            mrp=float(data['mrp']),
            sale_price=float(data['sale_price']),
            image=data['image'],
            description=data['description'],
            slug=data['slug']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'product created'}), 201
    
    except Exception as e:
        return jsonify({'message': 'error adding product'}), 500
    
