from flask import Blueprint, request, jsonify
from app.models.models import Cart, Product
from app import db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not user_id or not product_id or not quantity or quantity <= 0:
        return jsonify({"error": "Invalid input"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    db.session.commit()

    return jsonify({"message": "Product added to cart"}), 200

@cart_bp.route('/update', methods=['PUT'])
def update_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not user_id or not product_id or quantity is None or quantity < 0:
        return jsonify({"error": "Invalid input"}), 400

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return jsonify({"error": "Cart item not found"}), 404

    if quantity == 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    db.session.commit()

    return jsonify({"message": "Cart updated successfully"}), 200

@cart_bp.route('/delete', methods=['DELETE'])
def delete_from_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return jsonify({"error": "Cart item not found"}), 404

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"message": "Product removed from cart"}), 200

@cart_bp.route('/', methods=['GET'])
def get_cart():
    user_id = request.args.get('user_id')
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 404

    cart_details = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        cart_details.append({
            "product_id": product.id,
            "name": product.name,
            "quantity": item.quantity,
            "price": product.price,
            "total_price": item.quantity * product.price
        })

    return jsonify({"cart": cart_details}), 200
