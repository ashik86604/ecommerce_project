from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db_connection
from utils.auth_utils import login_required

address_bp = Blueprint('address', __name__, url_prefix='/addresses')

@address_bp.route('/')
@login_required
def list_addresses():
    """List all user addresses"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM addresses 
        WHERE user_id = %s
        ORDER BY is_default DESC
    """, (session['user_id'],))
    
    addresses = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('addresses/list.html', addresses=addresses)

@address_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_address():
    """Add new address"""
    if request.method == 'POST':
        street_address = request.form.get('street_address', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        postal_code = request.form.get('postal_code', '').strip()
        phone = request.form.get('phone', '').strip()
        address_type = request.form.get('address_type', 'home')
        is_default = request.form.get('is_default') == 'on'
        
        # Validation
        if not all([street_address, city, state, postal_code, phone]):
            flash("All fields are required", 'danger')
            return render_template('addresses/add.html')
        
        conn = get_db_connection()
        if not conn:
            flash("Database connection failed", 'danger')
            return render_template('addresses/add.html')
        
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO addresses (user_id, street_address, city, state, postal_code, phone, address_type, is_default)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (session['user_id'], street_address, city, state, postal_code, phone, address_type, is_default))
            
            conn.commit()
            flash("Address added successfully!", 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('address.list_addresses'))
            
        except Exception as e:
            conn.rollback()
            flash(f"Error adding address: {str(e)}", 'danger')
            cursor.close()
            conn.close()
            return render_template('addresses/add.html')
    
    return render_template('addresses/add.html')

@address_bp.route('/delete/<int:address_id>', methods=['POST'])
@login_required
def delete_address(address_id):
    """Delete address"""
    conn = get_db_connection()
    if not conn:
        return redirect(url_for('address.list_addresses'))
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            DELETE FROM addresses 
            WHERE address_id = %s AND user_id = %s
        """, (address_id, session['user_id']))
        
        conn.commit()
        flash("Address deleted successfully!", 'success')
    except Exception as e:
        conn.rollback()
        flash(f"Error deleting address: {str(e)}", 'danger')
    
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('address.list_addresses'))