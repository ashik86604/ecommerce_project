from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db_connection
from utils.auth_utils import role_required
import os
from werkzeug.utils import secure_filename
from config import Config
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ===== DASHBOARD ROUTES =====

@admin_bp.route('/dashboard')
@role_required('super_admin', 'product_manager', 'order_manager', 'payment_manager', 'delivery_manager')
def dashboard():
    """Admin dashboard - Role based"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    role = session.get('role')
    
    # Get dashboard statistics
    if role in ['super_admin', 'product_manager']:
        cursor.execute("SELECT COUNT(*) as total_products FROM products")
        total_products = cursor.fetchone()['total_products']
        
        cursor.execute("SELECT COUNT(*) as total_categories FROM categories")
        total_categories = cursor.fetchone()['total_categories']
        
        cursor.execute("SELECT COUNT(*) as low_stock FROM products WHERE stock_quantity < 10")
        low_stock = cursor.fetchone()['low_stock']
    else:
        total_products = total_categories = low_stock = 0
    
    if role in ['super_admin', 'order_manager']:
        cursor.execute("SELECT COUNT(*) as total_orders FROM orders")
        total_orders = cursor.fetchone()['total_orders']
        
        cursor.execute("SELECT COUNT(*) as pending_orders FROM orders WHERE order_status = 'placed'")
        pending_orders = cursor.fetchone()['pending_orders']
        
        cursor.execute("SELECT COUNT(*) as verified_orders FROM orders WHERE order_status = 'payment_verified'")
        verified_orders = cursor.fetchone()['verified_orders']
    else:
        total_orders = pending_orders = verified_orders = 0
    
    if role in ['super_admin', 'payment_manager']:
        cursor.execute("SELECT COUNT(*) as total_payments FROM payments")
        total_payments = cursor.fetchone()['total_payments']
        
        cursor.execute("SELECT COUNT(*) as pending_payments FROM payments WHERE payment_status = 'pending'")
        pending_payments = cursor.fetchone()['pending_payments']
        
        cursor.execute("SELECT SUM(payment_amount) as total_revenue FROM payments WHERE payment_status = 'success'")
        result = cursor.fetchone()
        total_revenue = result['total_revenue'] or 0
    else:
        total_payments = pending_payments = total_revenue = 0
    
    if role in ['super_admin', 'delivery_manager']:
        cursor.execute("SELECT COUNT(*) as total_deliveries FROM delivery_tracking WHERE status IN ('in_transit', 'out_for_delivery')")
        total_deliveries = cursor.fetchone()['total_deliveries']
        
        cursor.execute("SELECT COUNT(*) as delivered FROM delivery_tracking WHERE status = 'delivered'")
        delivered = cursor.fetchone()['delivered']
        
        cursor.execute("SELECT COUNT(*) as in_transit FROM delivery_tracking WHERE status = 'in_transit'")
        in_transit = cursor.fetchone()['in_transit']
    else:
        total_deliveries = delivered = in_transit = 0
    
    cursor.execute("SELECT COUNT(*) as total_customers FROM users WHERE role = 'customer'")
    total_customers = cursor.fetchone()['total_customers']
    
    cursor.close()
    conn.close()
    
    return render_template(
        'admin/dashboard.html',
        role=role,
        total_products=total_products,
        total_categories=total_categories,
        low_stock=low_stock,
        total_orders=total_orders,
        pending_orders=pending_orders,
        verified_orders=verified_orders,
        total_payments=total_payments,
        pending_payments=pending_payments,
        total_revenue=total_revenue,
        total_deliveries=total_deliveries,
        delivered=delivered,
        in_transit=in_transit,
        total_customers=total_customers
    )

# ===== PRODUCT MANAGEMENT =====

@admin_bp.route('/products')
@role_required('super_admin', 'product_manager')
def product_list():
    """List all products"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, c.category_name,
               (SELECT image_url FROM product_images WHERE product_id = p.product_id LIMIT 1) as image
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        ORDER BY p.created_at DESC
    """)
    
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/products/list.html', products=products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@role_required('super_admin', 'product_manager')
def add_product():
    """Add new product"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        product_name = request.form.get('product_name', '').strip()
        category_id = request.form.get('category_id')
        description = request.form.get('description', '').strip()
        price = request.form.get('price', 0, type=float)
        discount_price = request.form.get('discount_price', 0, type=float)
        stock_quantity = request.form.get('stock_quantity', 0, type=int)
        sku = request.form.get('sku', '').strip()
        
        errors = []
        if not product_name or len(product_name) < 3:
            errors.append("Product name must be at least 3 characters")
        if not category_id:
            errors.append("Category is required")
        if price <= 0:
            errors.append("Price must be greater than 0")
        if stock_quantity < 0:
            errors.append("Stock quantity cannot be negative")
        if 'product_images' not in request.files or len(request.files.getlist('product_images')) == 0:
            errors.append("At least one product image is required")
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            cursor.execute("SELECT category_id, category_name FROM categories WHERE is_active = TRUE")
            categories = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('admin/products/add.html', categories=categories)
        
        try:
            cursor.execute("""
                INSERT INTO products (category_id, product_name, description, price, discount_price, stock_quantity, sku, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (category_id, product_name, description, price, discount_price, stock_quantity, sku, session['user_id']))
            
            conn.commit()
            product_id = cursor.lastrowid
            
            images = request.files.getlist('product_images')
            for idx, image in enumerate(images):
                if image and image.filename and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    import time
                    filename = f"{product_id}_{int(time.time())}_{filename}"
                    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                    image.save(filepath)
                    
                    is_primary = idx == 0
                    cursor.execute("""
                        INSERT INTO product_images (product_id, image_url, is_primary)
                        VALUES (%s, %s, %s)
                    """, (product_id, f"/static/uploads/products/{filename}", is_primary))
                    conn.commit()
            
            flash("Product added successfully!", 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('admin.product_list'))
            
        except Exception as e:
            conn.rollback()
            flash(f"Error adding product: {str(e)}", 'danger')
            cursor.close()
            conn.close()
            return render_template('admin/products/add.html')
    
    cursor.execute("SELECT category_id, category_name FROM categories WHERE is_active = TRUE")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/products/add.html', categories=categories)

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@role_required('super_admin', 'product_manager')
def edit_product(product_id):
    """Edit product"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        cursor.close()
        conn.close()
        flash("Product not found", 'danger')
        return redirect(url_for('admin.product_list'))
    
    if request.method == 'POST':
        product_name = request.form.get('product_name', '').strip()
        category_id = request.form.get('category_id')
        description = request.form.get('description', '').strip()
        price = request.form.get('price', 0, type=float)
        discount_price = request.form.get('discount_price', 0, type=float)
        stock_quantity = request.form.get('stock_quantity', 0, type=int)
        sku = request.form.get('sku', '').strip()
        is_active = request.form.get('is_active') == 'on'
        
        try:
            cursor.execute("""
                UPDATE products 
                SET category_id = %s, product_name = %s, description = %s, 
                    price = %s, discount_price = %s, stock_quantity = %s, 
                    sku = %s, is_active = %s
                WHERE product_id = %s
            """, (category_id, product_name, description, price, discount_price, 
                  stock_quantity, sku, is_active, product_id))
            
            if 'product_images' in request.files:
                images = request.files.getlist('product_images')
                for image in images:
                    if image and image.filename and allowed_file(image.filename):
                        filename = secure_filename(image.filename)
                        import time
                        filename = f"{product_id}_{int(time.time())}_{filename}"
                        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                        image.save(filepath)
                        
                        cursor.execute("""
                            INSERT INTO product_images (product_id, image_url, is_primary)
                            VALUES (%s, %s, %s)
                        """, (product_id, f"/static/uploads/products/{filename}", False))
            
            conn.commit()
            flash("Product updated successfully!", 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('admin.product_list'))
            
        except Exception as e:
            conn.rollback()
            flash(f"Error updating product: {str(e)}", 'danger')
    
    cursor.execute("SELECT category_id, category_name FROM categories WHERE is_active = TRUE")
    categories = cursor.fetchall()
    
    cursor.execute("SELECT * FROM product_images WHERE product_id = %s", (product_id,))
    images = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('admin/products/edit.html', product=product, categories=categories, images=images)

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@role_required('super_admin', 'product_manager')
def delete_product(product_id):
    """Delete product"""
    conn = get_db_connection()
    if not conn:
        return redirect(url_for('admin.product_list'))
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        conn.commit()
        flash("Product deleted successfully!", 'success')
    except Exception as e:
        conn.rollback()
        flash(f"Error deleting product: {str(e)}", 'danger')
    
    cursor.close()
    conn.close()
    
    return redirect(url_for('admin.product_list'))

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# ===== CATEGORY MANAGEMENT =====

@admin_bp.route('/categories')
@role_required('super_admin', 'product_manager')
def category_list():
    """List all categories"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories ORDER BY category_name ASC")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/categories/list.html', categories=categories)

@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@role_required('super_admin', 'product_manager')
def add_category():
    """Add new category"""
    if request.method == 'POST':
        category_name = request.form.get('category_name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not category_name or len(category_name) < 3:
            flash("Category name must be at least 3 characters", 'danger')
            return render_template('admin/categories/add.html')
        
        conn = get_db_connection()
        if not conn:
            flash("Database connection failed", 'danger')
            return render_template('admin/categories/add.html')
        
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO categories (category_name, description)
                VALUES (%s, %s)
            """, (category_name, description))
            
            conn.commit()
            flash("Category added successfully!", 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('admin.category_list'))
            
        except Exception as e:
            conn.rollback()
            flash(f"Error adding category: {str(e)}", 'danger')
            cursor.close()
            conn.close()
    
    return render_template('admin/categories/add.html')

@admin_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@role_required('super_admin', 'product_manager')
def delete_category(category_id):
    """Delete category"""
    conn = get_db_connection()
    if not conn:
        return redirect(url_for('admin.category_list'))
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
        conn.commit()
        flash("Category deleted successfully!", 'success')
    except Exception as e:
        conn.rollback()
        flash(f"Error deleting category: {str(e)}", 'danger')
    
    cursor.close()
    conn.close()
    
    return redirect(url_for('admin.category_list'))

# ===== ORDER MANAGEMENT =====

@admin_bp.route('/orders')
@role_required('super_admin', 'order_manager')
def order_list():
    """List all orders"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Get filter
    status_filter = request.args.get('status', '')
    
    query = """
        SELECT o.*, u.username, u.email, COUNT(oi.order_item_id) as item_count
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
    """
    
    params = []
    if status_filter:
        query += " WHERE o.order_status = %s"
        params.append(status_filter)
    
    query += " GROUP BY o.order_id ORDER BY o.order_date DESC"
    
    cursor.execute(query, params)
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/orders/list.html', orders=orders, status_filter=status_filter)

@admin_bp.route('/orders/<int:order_id>')
@role_required('super_admin', 'order_manager')
def order_detail(order_id):
    """View order details"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.*, u.username, u.email, u.phone,
               a.street_address, a.city, a.state, a.postal_code
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        LEFT JOIN addresses a ON o.shipping_address_id = a.address_id
        WHERE o.order_id = %s
    """, (order_id,))
    
    order = cursor.fetchone()
    
    if not order:
        cursor.close()
        conn.close()
        flash("Order not found", 'danger')
        return redirect(url_for('admin.order_list'))
    
    # Get order items
    cursor.execute("""
        SELECT oi.*, p.product_name
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = %s
    """, (order_id,))
    
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/orders/detail.html', order=order, items=items)

@admin_bp.route('/orders/<int:order_id>/update-status', methods=['POST'])
@role_required('super_admin', 'order_manager')
def update_order_status(order_id):
    """Update order status"""
    new_status = request.form.get('status')
    
    # valid_statuses = ['placed', 'payment_verified', 'processing', 'shipped', 'delivered', 'cancelled']
    valid_statuses = ['placed','payment_verified','processing','packed','shipped','out_for_delivery','delivered','cancelled']
    if new_status not in valid_statuses:
        flash("Invalid status", 'danger')
        return redirect(url_for('admin.order_detail', order_id=order_id))
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed", 'danger')
        return redirect(url_for('admin.order_detail', order_id=order_id))
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE orders SET order_status = %s WHERE order_id = %s
        """, (new_status, order_id))
        
        # Add tracking record
        delivery_statuses = [
        'processing',
        'packed',
        'shipped',
        'out_for_delivery',
        'delivered',
        'cancelled'
        ]

        if new_status in delivery_statuses:
            cursor.execute("""
            INSERT INTO delivery_tracking (order_id, status, location, updated_by)
            VALUES (%s, %s, 'Order Updated', %s)
            """, (order_id, new_status, session['user_id']))
            # cursor.execute("""
            #     INSERT INTO delivery_tracking (order_id, status, location, updated_by)
            #     VALUES (%s, %s, 'Order Updated', %s)
            # """, (order_id, new_status, session['user_id']))
            conn.commit()
            flash(f"Order status updated to {new_status}!", 'success')
    except Exception as e:
        conn.rollback()
        flash(f"Error updating order: {str(e)}", 'danger')
    
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('admin.order_detail', order_id=order_id))

# ===== PAYMENT MANAGEMENT =====

@admin_bp.route('/payments')
@role_required('super_admin', 'payment_manager')
def payment_list():
    """List all payments"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Get filter
    status_filter = request.args.get('status', '')
    
    query = """
        SELECT p.*, o.order_id, u.username, u.email
        FROM payments p
        JOIN orders o ON p.order_id = o.order_id
        JOIN users u ON o.user_id = u.user_id
    """
    
    params = []
    if status_filter:
        query += " WHERE p.payment_status = %s"
        params.append(status_filter)
    
    query += " ORDER BY p.payment_date DESC"
    
    cursor.execute(query, params)
    payments = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/payments/list.html', payments=payments, status_filter=status_filter)

@admin_bp.route('/payments/<int:payment_id>')
@role_required('super_admin', 'payment_manager')
def payment_detail(payment_id):
    """View payment details"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, o.order_id, o.total_amount, u.username, u.email
        FROM payments p
        JOIN orders o ON p.order_id = o.order_id
        JOIN users u ON o.user_id = u.user_id
        WHERE p.payment_id = %s
    """, (payment_id,))
    
    payment = cursor.fetchone()
    
    if not payment:
        cursor.close()
        conn.close()
        flash("Payment not found", 'danger')
        return redirect(url_for('admin.payment_list'))
    
    # Get refunds if any
    cursor.execute("""
        SELECT * FROM refunds WHERE order_id = %s
    """, (payment['order_id'],))
    
    refunds = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/payments/detail.html', payment=payment, refunds=refunds)

@admin_bp.route('/payments/<int:payment_id>/refund', methods=['POST'])
@role_required('super_admin', 'payment_manager')
def refund_payment(payment_id):
    """Process refund"""
    refund_reason = request.form.get('reason', 'Customer requested refund')
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed", 'danger')
        return redirect(url_for('admin.payment_detail', payment_id=payment_id))
    
    cursor = conn.cursor(dictionary=True)
    
    # Get payment details
    cursor.execute("SELECT * FROM payments WHERE payment_id = %s", (payment_id,))
    payment = cursor.fetchone()
    
    if not payment:
        cursor.close()
        conn.close()
        flash("Payment not found", 'danger')
        return redirect(url_for('admin.payment_list'))
    
    if payment['payment_status'] != 'success':
        cursor.close()
        conn.close()
        flash("Cannot refund this payment", 'danger')
        return redirect(url_for('admin.payment_detail', payment_id=payment_id))
    
    try:
        # Create refund record
        # cursor.execute("""
        #     INSERT INTO refunds (order_id, refund_amount, refund_status, refund_reason, processed_by)
        #     VALUES (%s, %s, 'processed', %s, %s)
        # """, (payment['order_id'], payment['payment_amount'], refund_reason, session['user_id']))
        cursor.execute("""
        INSERT INTO refunds 
        (order_id, refund_amount, refund_reason, refund_status)
        VALUES (%s, %s, %s, 'processed')
        """, (payment['order_id'], payment['payment_amount'], refund_reason))
        # Update payment status
        cursor.execute("""
            UPDATE payments SET payment_status = 'refunded' WHERE payment_id = %s
        """, (payment_id,))
        
        # Update order status
        cursor.execute("""
            UPDATE orders SET payment_status = 'refunded' WHERE order_id = %s
        """, (payment['order_id'],))
        
        conn.commit()
        flash("Refund processed successfully!", 'success')
    except Exception as e:
        conn.rollback()
        flash(f"Error processing refund: {str(e)}", 'danger')
    
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('admin.payment_detail', payment_id=payment_id))

# ===== DELIVERY MANAGEMENT =====

@admin_bp.route('/deliveries')
@role_required('super_admin', 'delivery_manager')
def delivery_list():
    """List all deliveries"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Get filter
    status_filter = request.args.get('status', '')
    
    query = """
        SELECT DISTINCT dt.*, o.order_id, u.username, u.email
        FROM delivery_tracking dt
        JOIN orders o ON dt.order_id = o.order_id
        JOIN users u ON o.user_id = u.user_id
    """
    
    params = []
    if status_filter:
        query += " WHERE dt.status = %s"
        params.append(status_filter)
    
    query += " ORDER BY dt.status_update_date DESC"
    
    cursor.execute(query, params)
    deliveries = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/deliveries/list.html', deliveries=deliveries, status_filter=status_filter)

@admin_bp.route('/deliveries/<int:order_id>')
@role_required('super_admin', 'delivery_manager')
def delivery_detail(order_id):
    """View delivery tracking"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Get order
    cursor.execute("""
        SELECT o.*, u.username, u.email, u.phone,
               a.street_address, a.city, a.state, a.postal_code
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        LEFT JOIN addresses a ON o.shipping_address_id = a.address_id
        WHERE o.order_id = %s
    """, (order_id,))
    
    order = cursor.fetchone()
    
    if not order:
        cursor.close()
        conn.close()
        flash("Order not found", 'danger')
        return redirect(url_for('admin.delivery_list'))
    
    # Get tracking records
    cursor.execute("""
        SELECT * FROM delivery_tracking 
        WHERE order_id = %s
        ORDER BY status_update_date DESC
    """, (order_id,))
    
    tracking = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/deliveries/detail.html', order=order, tracking=tracking)

@admin_bp.route('/deliveries/<int:order_id>/update', methods=['POST'])
@role_required('super_admin', 'delivery_manager')
def update_delivery(order_id):
    """Update delivery status"""
    status = request.form.get('status')
    location = request.form.get('location', '').strip()
    notes = request.form.get('notes', '').strip()
    
    # valid_statuses = ['order_placed', 'processing', 'in_transit', 'out_for_delivery', 'delivered', 'cancelled']
    valid_statuses = ['processing','packed','shipped','out_for_delivery','delivered','cancelled']
    
    if status not in valid_statuses:
        flash("Invalid status", 'danger')
        return redirect(url_for('admin.delivery_detail', order_id=order_id))
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed", 'danger')
        return redirect(url_for('admin.delivery_detail', order_id=order_id))
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO delivery_tracking (order_id, status, location, notes, updated_by)
            VALUES (%s, %s, %s, %s, %s)
        """, (order_id, status, location, notes, session['user_id']))
        
        # Update order status if delivery is complete
        if status == 'delivered':
            cursor.execute("""
                UPDATE orders SET order_status = 'delivered' WHERE order_id = %s
            """, (order_id,))
        
        conn.commit()
        flash(f"Delivery status updated to {status}!", 'success')
    except Exception as e:
        conn.rollback()
        flash(f"Error updating delivery: {str(e)}", 'danger')
    
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('admin.delivery_detail', order_id=order_id))

# ===== ADMIN USER MANAGEMENT (Super Admin Only) =====

@admin_bp.route('/users')
@role_required('super_admin')
def user_list():
    """List all admin users (Super Admin only)"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT user_id, username, email, role, is_active, created_at
        FROM users
        WHERE role != 'customer'
        ORDER BY created_at DESC
    """)
    
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('admin/users/list.html', users=users)

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@role_required('super_admin')
def add_admin_user():
    """Add new admin user"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'product_manager')
        
        if not all([username, email, password]):
            flash("All fields required", 'danger')
            return render_template('admin/users/add.html')
        
        if len(password) < 6:
            flash("Password must be at least 6 characters", 'danger')
            return render_template('admin/users/add.html')
        
        valid_roles = ['super_admin', 'product_manager', 'order_manager', 'payment_manager', 'delivery_manager']
        if role not in valid_roles:
            flash("Invalid role", 'danger')
            return render_template('admin/users/add.html')
        
        conn = get_db_connection()
        if not conn:
            flash("Database connection failed", 'danger')
            return render_template('admin/users/add.html')
        
        cursor = conn.cursor()
        
        try:
            from utils.auth_utils import hash_password
            password_hash = hash_password(password)
            
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role, first_name, last_name)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (username, email, password_hash, role, username, 'Admin'))
            
            conn.commit()
            flash(f"Admin user '{username}' created successfully!", 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('admin.user_list'))
            
        except Exception as e:
            conn.rollback()
            flash(f"Error: {str(e)}", 'danger')
            cursor.close()
            conn.close()
            return render_template('admin/users/add.html')
    
    return render_template('admin/users/add.html')