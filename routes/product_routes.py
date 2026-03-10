from flask import Blueprint, render_template, request, jsonify, session
from database import get_db_connection
from utils.auth_utils import login_required

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/')
def list_products():
    """Display all products with search and filter functionality"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Get filters from query parameters
    search = request.args.get('search', '').strip()
    category_id = request.args.get('category', '')
    sort_by = request.args.get('sort', 'latest')
    page = request.args.get('page', 1, type=int)
    
    # Items per page
    items_per_page = 12
    offset = (page - 1) * items_per_page
    
    # Build query
    where_clause = "WHERE p.is_active = TRUE"
    params = []
    
    if search:
        where_clause += " AND (p.product_name LIKE %s OR p.description LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])
    
    if category_id:
        where_clause += " AND p.category_id = %s"
        params.append(category_id)
    
    # Sort options
    if sort_by == 'price_low':
        order_by = "ORDER BY COALESCE(p.discount_price, p.price) ASC"
    elif sort_by == 'price_high':
        order_by = "ORDER BY COALESCE(p.discount_price, p.price) DESC"
    elif sort_by == 'rating':
        order_by = "ORDER BY p.rating DESC"
    else:  # latest
        order_by = "ORDER BY p.created_at DESC"
    
    # Get total count
    cursor.execute(f"SELECT COUNT(*) as count FROM products p {where_clause}", params)
    total_products = cursor.fetchone()['count']
    total_pages = (total_products + items_per_page - 1) // items_per_page
    
    # Get products with images
    query = f"""
        SELECT p.*, c.category_name,
               (SELECT image_url FROM product_images 
                WHERE product_id = p.product_id AND is_primary = TRUE LIMIT 1) as primary_image
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        {where_clause}
        {order_by}
        LIMIT %s OFFSET %s
    """
    params.extend([items_per_page, offset])
    
    cursor.execute(query, params)
    products = cursor.fetchall()
    
    # Get all categories for filter
    cursor.execute("SELECT category_id, category_name FROM categories WHERE is_active = TRUE")
    categories = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template(
        'products/list.html',
        products=products,
        categories=categories,
        search=search,
        category_id=category_id,
        sort_by=sort_by,
        page=page,
        total_pages=total_pages
    )

@product_bp.route('/<int:product_id>')
def product_detail(product_id):
    """Display product details"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Get product details
    cursor.execute("""
        SELECT p.*, c.category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE p.product_id = %s AND p.is_active = TRUE
    """, (product_id,))
    
    product = cursor.fetchone()
    
    if not product:
        cursor.close()
        conn.close()
        return "Product not found", 404
    
    # Get product images
    cursor.execute("""
        SELECT image_id, image_url, is_primary 
        FROM product_images 
        WHERE product_id = %s 
        ORDER BY is_primary DESC
    """, (product_id,))
    
    images = cursor.fetchall()
    
    # Get product reviews/feedback
    cursor.execute("""
        SELECT f.rating, f.comment, u.username, f.created_at
        FROM feedback f
        LEFT JOIN users u ON f.user_id = u.user_id
        WHERE f.product_id = %s
        ORDER BY f.created_at DESC
    """, (product_id,))
    
    reviews = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template(
        'products/detail.html',
        product=product,
        images=images,
        reviews=reviews
    )