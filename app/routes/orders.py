from flask import Blueprint, request, jsonify
from app.models.models import Order, Cart, Product
from app import db

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/placeorder', methods=['POST'])
def place_order():
    data = request.get_json()
    user_id = data.get('user_id')
    shipping_details = data.get('shipping_details')

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    total_amount = 0
    for item in cart_items:
        product = Product.query.get(item.product_id)
        total_amount += item.quantity * product.price

    order = Order(user_id=user_id, shipping_details=shipping_details, total_amount=total_amount)
    db.session.add(order)

    # Clear the cart
    for item in cart_items:
        db.session.delete(item)

    db.session.commit()

    return jsonify({"message": "Order placed successfully", "order_id": order.id}), 201
