from flask import Blueprint, request, jsonify
from app.models.models import Product
from app import db

products_bp = Blueprint('products', __name__)

@products_bp.route('/addproduct', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category = data.get('category')

    if not name or not description or not price or not category:
        return jsonify({"error": "All fields are required"}), 400

    if price <= 0:
        return jsonify({"error": "Price must be a positive number"}), 400

    product = Product(name=name, description=description, price=price, category=category)
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product added successfully", "product_id": product.id}), 201

@products_bp.route('/updateproduct/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.category = data.get('category', product.category)
    db.session.commit()

    return jsonify({"message": "Product updated successfully"}), 200

@products_bp.route('/deleteproduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200

@products_bp.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    if not products:
        return jsonify({"message": "No products found"}), 404

    product_list = [{"id": p.id, "name": p.name, "description": p.description, "price": p.price, "category": p.category} for p in products]
    return jsonify({"products": product_list}), 200
