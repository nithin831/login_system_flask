from flask import Blueprint, render_template, request, make_response, jsonify
from models import Product
from db import db

view = Blueprint('view', __name__)

@view.route('/products', methods=['GET'])
def get_products():
    try:
        page = request.args.get('page', 1, type=int)
        print(page)
        per_page = request.args.get('per_page', 2, type=int)
        category = request.args.get('category')
        tags = request.args.get('tags')
        search = request.args.get('search')

        query = Product.query

        if category:
            query = query.filter(Product.category == category)
        if tags:
            query = query.filter(Product.tags.contains(tags))
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return make_response(jsonify([prod.json() for prod in pagination]), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting product'}), 500)
    
        
