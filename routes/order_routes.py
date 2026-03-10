from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session, jsonify
from database import get_db_connection
from utils.auth_utils import login_required
from datetime import datetime, timedelta
from decimal import Decimal
from utils.razorpay_utils import create_razorpay_order, verify_razorpay_payment

order_bp = Blueprint('order', __name__, url_prefix='/orders')

@order_bp.route('/')
@login_required
def list_orders():
    """List all orders for logged-in user"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.*, COUNT(oi.order_item_id) as item_count
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.user_id = %s
        GROUP BY o.order_id
        ORDER BY o.order_date DESC
    """, (session['user_id'],))
    
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('orders/list.html', orders=orders)

@order_bp.route('/<int:order_id>')
@login_required
def order_detail(order_id):
    """View order details"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Get order
    cursor.execute("""
        SELECT * FROM orders 
        WHERE order_id = %s AND user_id = %s
    """, (order_id, session['user_id']))
    
    order = cursor.fetchone()
    
    if not order:
        cursor.close()
        conn.close()
        flash("Order not found", 'danger')
        return redirect(url_for('order.list_orders'))
    
    # Get order items
    cursor.execute("""
        SELECT oi.*, p.product_name, p.product_id
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = %s
    """, (order_id,))
    
    items = cursor.fetchall()
    
    # Get delivery tracking
    cursor.execute("""
        SELECT * FROM delivery_tracking 
        WHERE order_id = %s 
        ORDER BY status_update_date DESC
    """, (order_id,))
    
    tracking = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('orders/detail.html', order=order, items=items, tracking=tracking)

#checkout
@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page"""
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed", 'danger')
        return redirect(url_for('cart.view_cart'))
    
    cursor = conn.cursor(dictionary=True)
    
    # Get user's cart
    cursor.execute("""
        SELECT c.cart_id FROM cart c 
        WHERE c.user_id = %s
    """, (session['user_id'],))
    
    cart = cursor.fetchone()
    
    if not cart:
        flash("Your cart is empty", 'warning')
        cursor.close()
        conn.close()
        return redirect(url_for('cart.view_cart'))
    
    # Get cart items
    cursor.execute("""
        SELECT ci.cart_item_id, ci.product_id, ci.quantity, ci.price,
               p.product_name, p.stock_quantity
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.product_id
        WHERE ci.cart_id = %s
    """, (cart['cart_id'],))
    
    cart_items = cursor.fetchall()
    
    if not cart_items:
        flash("Your cart is empty", 'warning')
        cursor.close()
        conn.close()
        return redirect(url_for('cart.view_cart'))
    
    # Get user's addresses
    cursor.execute("""
        SELECT * FROM addresses 
        WHERE user_id = %s
        ORDER BY is_default DESC
    """, (session['user_id'],))
    
    addresses = cursor.fetchall()
    
    # Calculate totals
    subtotal = Decimal('0')
    for item in cart_items:
        price = Decimal(str(item['price']))
        quantity = Decimal(str(item['quantity']))
        subtotal += price * quantity
    
    shipping = Decimal('50') if subtotal > 0 else Decimal('0')
    tax = subtotal * Decimal('0.05')
    total = subtotal + shipping + tax
    
    if request.method == 'POST':
        # Get form data
        address_id = request.form.get('address_id')
        payment_method = request.form.get('payment_method')
        
        # Check if user has addresses
        if not addresses:
            flash("Please add a delivery address first", 'danger')
            return render_template('orders/checkout.html', 
                                 cart_items=cart_items, 
                                 addresses=addresses,
                                 subtotal=float(subtotal),
                                 shipping=float(shipping),
                                 tax=float(tax),
                                 total=float(total))
        
        # Validation
        if not address_id:
            flash("Please select a delivery address", 'danger')
            return render_template('orders/checkout.html', 
                                 cart_items=cart_items, 
                                 addresses=addresses,
                                 subtotal=float(subtotal),
                                 shipping=float(shipping),
                                 tax=float(tax),
                                 total=float(total))
        
        if not payment_method or payment_method not in ['upi', 'card']:
            flash("Please select a valid payment method", 'danger')
            return render_template('orders/checkout.html', 
                                 cart_items=cart_items, 
                                 addresses=addresses,
                                 subtotal=float(subtotal),
                                 shipping=float(shipping),
                                 tax=float(tax),
                                 total=float(total))
        
        try:
            # Create order
            cursor.execute("""
                INSERT INTO orders 
                (user_id, total_amount, shipping_address_id, order_status, payment_method, payment_status, estimated_delivery)
                VALUES (%s, %s, %s, 'placed', %s, 'pending', %s)
            """, (session['user_id'], float(total), address_id, payment_method, 
                  (datetime.now() + timedelta(days=5)).date()))
            
            conn.commit()
            order_id = cursor.lastrowid
            
            # Add order items
            for item in cart_items:
                cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                """, (order_id, item['product_id'], item['quantity'], 
                      float(item['price']), float(item['price']) * item['quantity']))
            
            # Create delivery tracking record
            cursor.execute("""
                INSERT INTO delivery_tracking (order_id, status, location, updated_by)
                VALUES (%s, 'processing', 'Order Placed', %s)
            """, (order_id, session['user_id']))
            
            conn.commit()
            
            # Redirect to payment page
            cursor.close()
            conn.close()
            return redirect(url_for('order.payment', order_id=order_id))
            
        except Exception as e:
            conn.rollback()
            flash(f"Error creating order: {str(e)}", 'danger')
            cursor.close()
            conn.close()
            return redirect(url_for('order.checkout'))
    
    cursor.close()
    conn.close()
    
    return render_template('orders/checkout.html', 
                         cart_items=cart_items,
                         addresses=addresses,
                         subtotal=float(subtotal),
                         shipping=float(shipping),
                         tax=float(tax),
                         total=float(total))


# @order_bp.route('/<int:order_id>/payment', methods=['GET', 'POST'])
# @login_required
# def payment(order_id):
#     """Payment page with Razorpay integration"""
#     conn = get_db_connection()
#     if not conn:
#         flash("Database connection failed", 'danger')
#         return redirect(url_for('order.list_orders'))
    
#     cursor = conn.cursor(dictionary=True)
    
#     # Get order
#     cursor.execute("""
#         SELECT * FROM orders 
#         WHERE order_id = %s AND user_id = %s
#     """, (order_id, session['user_id']))
    
#     order = cursor.fetchone()
    
#     if not order:
#         cursor.close()
#         conn.close()
#         flash("Order not found", 'danger')
#         return redirect(url_for('order.list_orders'))
    
#     # Get user details
#     cursor.execute("""
#         SELECT email, phone FROM users WHERE user_id = %s
#     """, (session['user_id'],))
    
#     user = cursor.fetchone()
    
#     if request.method == 'POST':
#         try:
#             # Create Razorpay order
#             razorpay_order = create_razorpay_order(
#                 amount=order['total_amount'],
#                 order_id=order_id,
#                 user_email=user['email'],
#                 user_phone=user['phone'] or '9999999999'  # Default if phone is null
#             )
            
#             # Store Razorpay order ID in database
#             cursor.execute("""
#                 UPDATE orders 
#                 SET razorpay_order_id = %s
#                 WHERE order_id = %s
#             """, (razorpay_order['id'], order_id))
            
#             conn.commit()
            
#             # Pass Razorpay details to frontend
#             cursor.close()
#             conn.close()
            
#             return render_template('orders/payment.html', 
#                                  order=order,
#                                  razorpay_order=razorpay_order,
#                                  user_email=user['email'],
#                                  user_phone=user['phone'] or '9999999999')
        
#         except Exception as e:
#             flash(f"Error initializing payment: {str(e)}", 'danger')
#             cursor.close()
#             conn.close()
#             return render_template('orders/payment.html', order=order)
    
#     cursor.close()
#     conn.close()
#     return render_template('orders/payment.html', order=order)
@order_bp.route('/<int:order_id>/payment')
@login_required
def payment(order_id):

    conn = get_db_connection()
    if not conn:
        flash("Database connection failed", 'danger')
        return redirect(url_for('order.list_orders'))

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM orders 
        WHERE order_id = %s AND user_id = %s
    """, (order_id, session['user_id']))

    order = cursor.fetchone()

    if not order:
        cursor.close()
        conn.close()
        flash("Order not found", 'danger')
        return redirect(url_for('order.list_orders'))

    cursor.execute("""
        SELECT email, phone FROM users WHERE user_id = %s
    """, (session['user_id'],))

    user = cursor.fetchone()

    try:

        razorpay_order = create_razorpay_order(
            amount=order['total_amount'],
            order_id=order_id,
            user_email=user['email'],
            user_phone=user['phone'] or '9999999999'
        )

        cursor.execute("""
            UPDATE orders
            SET razorpay_order_id = %s
            WHERE order_id = %s
        """, (razorpay_order['id'], order_id))

        conn.commit()

        return render_template(
            "orders/payment.html",
            order=order,
            razorpay_order=razorpay_order,
            user_email=user['email'],
            user_phone=user['phone'] or '9999999999',
            razorpay_key=current_app.config["RAZORPAY_KEY_ID"]
        )

    except Exception as e:
        flash(f"Payment initialization failed: {str(e)}", "danger")
        return redirect(url_for("order.list_orders"))

    finally:
        cursor.close()
        conn.close()

@order_bp.route('/<int:order_id>/verify-payment', methods=['POST'])
@login_required
def verify_payment(order_id):
    """Verify Razorpay payment signature"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get order
        cursor.execute("""
            SELECT * FROM orders 
            WHERE order_id = %s AND user_id = %s
        """, (order_id, session['user_id']))
        
        order = cursor.fetchone()
        
        if not order:
            return jsonify({'success': False, 'message': 'Order not found'}), 404
        
        # Get payment details from request
        data = request.get_json()
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        print(f"Verifying payment: Order ID: {razorpay_order_id}, Payment ID: {razorpay_payment_id}")
        
        # Verify payment signature
        if not verify_razorpay_payment(razorpay_order_id, razorpay_payment_id, razorpay_signature):
            print("Signature verification failed!")
            return jsonify({'success': False, 'message': 'Payment verification failed - Invalid signature'}), 400
        
        print("Signature verified successfully!")
        
        # Update order with payment details
        try:
            cursor.execute("""
                INSERT INTO payments (order_id, payment_amount, payment_method, transaction_id, payment_status)
                VALUES (%s, %s, %s, %s, 'success')
            """, (order_id, order['total_amount'], 'upi', razorpay_payment_id))
            # (order_id, order['total_amount'], 'razorpay', razorpay_payment_id))
            
            # Update order status
            cursor.execute("""
                UPDATE orders 
                SET payment_status = 'verified', order_status = 'payment_verified'
                WHERE order_id = %s
            """, (order_id,))
            
            print(f"Order {order_id} payment status updated to verified!")
            
            # Update delivery tracking
            cursor.execute("""
                INSERT INTO delivery_tracking (order_id, status, location, updated_by)
                VALUES (%s, 'processing', 'Payment Verified', %s)
            """, (order_id, session['user_id']))
            
            # Clear cart
            cursor.execute("SELECT cart_id FROM cart WHERE user_id = %s", (session['user_id'],))
            cart = cursor.fetchone()
            if cart:
                cursor.execute("DELETE FROM cart_items WHERE cart_id = %s", (cart['cart_id'],))
            
            conn.commit()
            print("Payment verification and order update completed successfully!")
            
            return jsonify({'success': True, 'message': 'Payment verified successfully'}), 200
        
        except Exception as db_error:
            conn.rollback()
            print(f"Database error: {str(db_error)}")
            return jsonify({'success': False, 'message': f'Database error: {str(db_error)}'}), 500
    
    except Exception as e:
        print(f"Error in verify_payment: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    
    finally:
        cursor.close()
        conn.close()

# # ADD this new route after the payment route
# @order_bp.route('/<int:order_id>/verify-payment', methods=['POST'])
# @login_required
# def verify_payment(order_id):
#     """Verify Razorpay payment signature"""
#     conn = get_db_connection()
#     if not conn:
#         return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    
#     cursor = conn.cursor(dictionary=True)
    
#     try:
#         # Get order
#         cursor.execute("""
#             SELECT * FROM orders 
#             WHERE order_id = %s AND user_id = %s
#         """, (order_id, session['user_id']))
        
#         order = cursor.fetchone()
        
#         if not order:
#             return jsonify({'success': False, 'message': 'Order not found'}), 404
        
#         # Get payment details from request
#         data = request.get_json()
#         razorpay_order_id = data.get('razorpay_order_id')
#         razorpay_payment_id = data.get('razorpay_payment_id')
#         razorpay_signature = data.get('razorpay_signature')
        
#         # Verify payment signature
#         if not verify_razorpay_payment(razorpay_order_id, razorpay_payment_id, razorpay_signature):
#             return jsonify({'success': False, 'message': 'Payment verification failed'}), 400
        
#         # Update order with payment details
#         cursor.execute("""
#             INSERT INTO payments (order_id, payment_amount, payment_method, transaction_id, payment_status)
#             VALUES (%s, %s, %s, %s, 'success')
#         """, (order_id, order['total_amount'], 'razorpay', razorpay_payment_id))
        
#         # Update order status
#         cursor.execute("""
#             UPDATE orders 
#             SET payment_status = 'verified', order_status = 'payment_verified'
#             WHERE order_id = %s
#         """, (order_id,))
        
#         # Update delivery tracking
#         cursor.execute("""
#             INSERT INTO delivery_tracking (order_id, status, location, updated_by)
#             VALUES (%s, 'payment_verified', 'Payment Verified', %s)
#         """, (order_id, session['user_id']))
        
#         # Clear cart
#         cursor.execute("SELECT cart_id FROM cart WHERE user_id = %s", (session['user_id'],))
#         cart = cursor.fetchone()
#         if cart:
#             cursor.execute("DELETE FROM cart_items WHERE cart_id = %s", (cart['cart_id'],))
        
#         conn.commit()
        
#         return jsonify({'success': True, 'message': 'Payment verified successfully'}), 200
    
#     except Exception as e:
#         conn.rollback()
#         return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
    
#     finally:
#         cursor.close()
#         conn.close()
# @order_bp.route('/<int:order_id>/payment', methods=['GET', 'POST'])
# @login_required
# def payment(order_id):
#     """Payment page"""
#     conn = get_db_connection()
#     if not conn:
#         flash("Database connection failed", 'danger')
#         return redirect(url_for('order.list_orders'))
    
#     cursor = conn.cursor(dictionary=True)
    
#     # Get order
#     cursor.execute("""
#         SELECT * FROM orders 
#         WHERE order_id = %s AND user_id = %s
#     """, (order_id, session['user_id']))
    
#     order = cursor.fetchone()
    
#     if not order:
#         cursor.close()
#         conn.close()
#         flash("Order not found", 'danger')
#         return redirect(url_for('order.list_orders'))
    
#     if request.method == 'POST':
#         # Simulate payment processing
#         transaction_id = f"TXN{order_id}{int(datetime.now().timestamp())}"
        
#         try:
#             # Create payment record
#             cursor.execute("""
#                 INSERT INTO payments (order_id, payment_amount, payment_method, transaction_id, payment_status)
#                 VALUES (%s, %s, %s, %s, 'success')
#             """, (order_id, order['total_amount'], order['payment_method'], transaction_id))
            
#             # Update order payment status
#             cursor.execute("""
#                 UPDATE orders 
#                 SET payment_status = 'verified', order_status = 'payment_verified'
#                 WHERE order_id = %s
#             """, (order_id,))
            
#             # Update delivery tracking
#             cursor.execute("""
#                 INSERT INTO delivery_tracking (order_id, status, location, updated_by)
#                 VALUES (%s, 'payment_verified', 'Payment Verified', %s)
#             """, (order_id, session['user_id']))
            
#             # Clear cart
#             cursor.execute("SELECT cart_id FROM cart WHERE user_id = %s", (session['user_id'],))
#             cart = cursor.fetchone()
#             if cart:
#                 cursor.execute("DELETE FROM cart_items WHERE cart_id = %s", (cart['cart_id'],))
            
#             conn.commit()
            
#             cursor.close()
#             conn.close()
            
#             flash("Payment successful! Your order has been placed.", 'success')
#             return redirect(url_for('order.order_confirmation', order_id=order_id))
            
#         except Exception as e:
#             conn.rollback()
#             flash(f"Payment error: {str(e)}", 'danger')
#             cursor.close()
#             conn.close()
#             return render_template('orders/payment.html', order=order)
    
#     cursor.close()
#     conn.close()
    
#     return render_template('orders/payment.html', order=order)

@order_bp.route('/<int:order_id>/confirmation')
@login_required
def order_confirmation(order_id):
    """Order confirmation page"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Get order
    cursor.execute("""
        SELECT * FROM orders 
        WHERE order_id = %s AND user_id = %s
    """, (order_id, session['user_id']))
    
    order = cursor.fetchone()
    
    if not order:
        cursor.close()
        conn.close()
        flash("Order not found", 'danger')
        return redirect(url_for('order.list_orders'))
    
    # Get order items
    cursor.execute("""
        SELECT oi.*, p.product_name, p.product_id
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = %s
    """, (order_id,))
    
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('orders/confirmation.html', order=order, items=items)

@order_bp.route('/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    """Cancel order and process refund"""
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed", 'danger')
        return redirect(url_for('order.list_orders'))
    
    cursor = conn.cursor(dictionary=True)
    
    # Get order
    cursor.execute("""
        SELECT * FROM orders 
        WHERE order_id = %s AND user_id = %s
    """, (order_id, session['user_id']))
    
    order = cursor.fetchone()
    
    if not order:
        cursor.close()
        conn.close()
        flash("Order not found", 'danger')
        return redirect(url_for('order.list_orders'))
    
    # Check if order can be cancelled
    if order['order_status'] in ['delivered', 'cancelled']:
        cursor.close()
        conn.close()
        flash("This order cannot be cancelled", 'danger')
        return redirect(url_for('order.order_detail', order_id=order_id))
    
    try:
        # Update order status
        cursor.execute("""
            UPDATE orders 
            SET order_status = 'cancelled', payment_status = 'refunded'
            WHERE order_id = %s
        """, (order_id,))
        
        # Create refund record
        cursor.execute("""
            INSERT INTO refunds (order_id, refund_amount, refund_status, refund_reason)
            VALUES (%s, %s, 'processed', 'Customer requested cancellation')
        """, (order_id, order['total_amount']))
        
        # Update delivery tracking
        cursor.execute("""
            INSERT INTO delivery_tracking (order_id, status, location, notes)
            VALUES (%s, 'cancelled', 'Order Cancelled', 'Customer requested cancellation')
        """, (order_id,))
        
        conn.commit()
        flash("Order cancelled successfully. Refund will be processed soon.", 'success')
        
    except Exception as e:
        conn.rollback()
        flash(f"Error cancelling order: {str(e)}", 'danger')
    
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('order.order_detail', order_id=order_id))