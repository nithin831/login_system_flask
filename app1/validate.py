import re
from flask import jsonify, make_response

def validate_product_data(data):
    # Validate name: length and no digits
    if 'name' not in data or not isinstance(data['name'], str) or not (3 < len(data['name']) < 100):
        return False, "Name must be more than 3 and less than 100 characters."
    if any(char.isdigit() for char in data['name']):
        return False, "Name must not contain digits."
    
    # Validate category
    if 'category' not in data or not isinstance(data['category'], str) or len(data['category']) > 50:
        return False, "Invalid category."

    # Validate tags (optional)
    if 'tags' in data and not isinstance(data['tags'], str):
        return False, "Tags should be a string."
    
    # Validate MRP
    if 'mrp' not in data or not isinstance(data['mrp'], (int)) or data['mrp'] <= 0:
        return False, "Invalid MRP."
    
    # Validate sale price
    if 'sale_price' not in data or not isinstance(data['sale_price'], (int  )) or data['sale_price'] <= 0:
        return False, "Invalid sale price."
    
    # Validate image URL (optional but should follow URL format if provided)
    if 'image' in data and data['image']:
        url_pattern = re.compile(
            r'^(https?://)?(www\.)?([A-Za-z0-9-._~:/?#[\]@!$&\'()*+,;=%]+)'
        )
        if not url_pattern.match(data['image']):
            return False, "Image must be a valid URL."
    
    # Validate description (optional but should be < 100 chars if provided)
    if 'description' in data and data['description'] and len(data['description']) > 100:
        return False, "Description must be less than 100 characters."
    
    # Validate slug
    if 'slug' not in data or not isinstance(data['slug'], str) or len(data['slug']) > 100:
        return False, "Invalid slug."

    return True, None

def validate_pagination(page, per_page):
    # Validate page
    try:
        page = int(page)
        print(page)
        if page < 1:
            return False, "Page number must be a positive integer."
    except ValueError:
        return False, "Page number must be an integer."

    # Validate per_page
    try:
        per_page = int(per_page)
        print(per_page)
        if per_page < 1 or per_page > 10:
            return False, "Per page must be between 1 and 10."
    except ValueError:
        return False, "Per page must be an integer."

    return True, None
    
    
# create a login system,
# docker, radis, poatgres, falsk, pyscopg2 
# user registrastion feature: email, password, name, role-> array of roles[member, admin, ].
# login: admin login, user login

# learning points: 