from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from database import get_db_connection
from decimal import Decimal

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

def get_or_create_cart(user_id):
    """Get existing cart or create new one"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if cart exists
    cursor.execute("SELECT cart_id FROM cart WHERE user_id = %s", (user_id,))
    cart = cursor.fetchone()
    
    if not cart:
        # Create new cart
        cursor.execute("INSERT INTO cart (user_id) VALUES (%s)", (user_id,))
        conn.commit()
        cart_id = cursor.lastrowid
    else:
        cart_id = cart[0]
    
    cursor.close()
    conn.close()
    return cart_id

@cart_bp.route('/')
def view_cart():
    """Display shopping cart"""
    if 'user_id' not in session:
        flash("Please login to view cart", 'warning')
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Get cart
    cursor.execute("SELECT cart_id FROM cart WHERE user_id = %s", (session['user_id'],))
    cart = cursor.fetchone()
    
    cart_items = []
    subtotal = Decimal('0')
    shipping = Decimal('0')
    tax = Decimal('0')
    total = Decimal('0')
    
    if cart:
        # Get cart items with product details
        cursor.execute("""
            SELECT ci.cart_item_id, ci.product_id, ci.quantity, ci.price,
                   p.product_name, p.stock_quantity,
                   (SELECT image_url FROM product_images 
                    WHERE product_id = p.product_id AND is_primary = TRUE LIMIT 1) as product_image
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.product_id
            WHERE ci.cart_id = %s
            ORDER BY ci.added_at DESC
        """, (cart['cart_id'],))
        
        cart_items = cursor.fetchall()
        
        # Calculate totals with proper Decimal handling
        if cart_items:
            for item in cart_items:
                price = Decimal(str(item['price']))
                quantity = Decimal(str(item['quantity']))
                subtotal += price * quantity
            
            shipping = Decimal('50') if subtotal > 0 else Decimal('0')  # Shipping charge
            tax = subtotal * Decimal('0.05')  # 5% tax
            total = subtotal + shipping + tax
    
    cursor.close()
    conn.close()
    
    return render_template(
        'cart/view.html',
        cart_items=cart_items,
        subtotal=float(subtotal),
        shipping=float(shipping),
        tax=float(tax),
        total=float(total)
    )

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    """Add product to cart (AJAX)"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login first'}), 401
    
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id or quantity < 1:
        return jsonify({'success': False, 'message': 'Invalid product or quantity'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database error'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Verify product exists and get price
    cursor.execute("""
        SELECT product_id, price, discount_price, stock_quantity 
        FROM products 
        WHERE product_id = %s AND is_active = TRUE
    """, (product_id,))
    
    product = cursor.fetchone()
    
    if not product:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    
    if product['stock_quantity'] < quantity:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Insufficient stock'}), 400
    
    # Get or create cart
    cart_id = get_or_create_cart(session['user_id'])
    
    # Get product price (use discount if available)
    price = product['discount_price'] if product['discount_price'] else product['price']
    
    # Check if product already in cart
    cursor.execute("""
        SELECT cart_item_id, quantity FROM cart_items 
        WHERE cart_id = %s AND product_id = %s
    """, (cart_id, product_id))
    
    existing_item = cursor.fetchone()
    
    if existing_item:
        # Update quantity
        new_quantity = existing_item['quantity'] + quantity
        if product['stock_quantity'] < new_quantity:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Insufficient stock'}), 400
        
        cursor.execute("""
            UPDATE cart_items 
            SET quantity = %s 
            WHERE cart_item_id = %s
        """, (new_quantity, existing_item['cart_item_id']))
    else:
        # Add new item
        cursor.execute("""
            INSERT INTO cart_items (cart_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (cart_id, product_id, quantity, price))
    
    conn.commit()
    
    # Get updated cart count
    cursor.execute("""
        SELECT SUM(quantity) as item_count FROM cart_items WHERE cart_id = %s
    """, (cart_id,))
    
    result = cursor.fetchone()
    item_count = result['item_count'] or 0
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': 'Product added to cart',
        'item_count': item_count
    })

@cart_bp.route('/update/<int:cart_item_id>', methods=['POST'])
def update_cart_item(cart_item_id):
    """Update cart item quantity"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login first'}), 401
    
    data = request.get_json()
    quantity = data.get('quantity', 1)
    
    if quantity < 1:
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database error'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Verify item belongs to user's cart
    cursor.execute("""
        SELECT ci.cart_item_id, ci.product_id, p.stock_quantity
        FROM cart_items ci
        JOIN cart c ON ci.cart_id = c.cart_id
        JOIN products p ON ci.product_id = p.product_id
        WHERE ci.cart_item_id = %s AND c.user_id = %s
    """, (cart_item_id, session['user_id']))
    
    item = cursor.fetchone()
    
    if not item:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Item not found'}), 404
    
    if item['stock_quantity'] < quantity:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Insufficient stock'}), 400
    
    # Update quantity
    cursor.execute("""
        UPDATE cart_items SET quantity = %s WHERE cart_item_id = %s
    """, (quantity, cart_item_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Cart updated'})

@cart_bp.route('/remove/<int:cart_item_id>', methods=['POST'])
def remove_from_cart(cart_item_id):
    """Remove item from cart"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login first'}), 401
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database error'}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Verify item belongs to user's cart
    cursor.execute("""
        SELECT ci.cart_item_id FROM cart_items ci
        JOIN cart c ON ci.cart_id = c.cart_id
        WHERE ci.cart_item_id = %s AND c.user_id = %s
    """, (cart_item_id, session['user_id']))
    
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Item not found'}), 404
    
    # Delete item
    cursor.execute("DELETE FROM cart_items WHERE cart_item_id = %s", (cart_item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Item removed from cart'})

@cart_bp.route('/count')
def get_cart_count():
    """Get cart item count (for navbar)"""
    if 'user_id' not in session:
        return jsonify({'count': 0})
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'count': 0})
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT SUM(quantity) as count FROM cart_items ci
        JOIN cart c ON ci.cart_id = c.cart_id
        WHERE c.user_id = %s
    """, (session['user_id'],))
    
    result = cursor.fetchone()
    count = result['count'] or 0
    
    cursor.close()
    conn.close()
    
    return jsonify({'count': count})