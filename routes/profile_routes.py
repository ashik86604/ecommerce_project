from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db_connection
from utils.auth_utils import login_required, hash_password
import re

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
@login_required
def view_profile():
    """View user profile"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM users WHERE user_id = %s
    """, (session['user_id'],))
    
    user = cursor.fetchone()
    
    # Get user's addresses
    cursor.execute("""
        SELECT * FROM addresses WHERE user_id = %s ORDER BY is_default DESC
    """, (session['user_id'],))
    
    addresses = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('profile/view.html', user=user, addresses=addresses)

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Validation
        if not all([first_name, last_name, email]):
            flash("All fields are required", 'danger')
            return render_template('profile/edit.html', user=user)
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash("Invalid email address", 'danger')
            return render_template('profile/edit.html', user=user)
        
        conn = get_db_connection()
        if not conn:
            flash("Database connection failed", 'danger')
            return render_template('profile/edit.html', user=user)
        
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE users 
                SET first_name = %s, last_name = %s, email = %s, phone = %s
                WHERE user_id = %s
            """, (first_name, last_name, email, phone, session['user_id']))
            
            conn.commit()
            flash("Profile updated successfully!", 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('profile.view_profile'))
            
        except Exception as e:
            conn.rollback()
            flash(f"Error updating profile: {str(e)}", 'danger')
            cursor.close()
            conn.close()
            return render_template('profile/edit.html', user=user)
    
    return render_template('profile/edit.html', user=user)

@profile_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not all([current_password, new_password, confirm_password]):
            flash("All fields are required", 'danger')
            return render_template('profile/change_password.html')
        
        if len(new_password) < 6:
            flash("New password must be at least 6 characters", 'danger')
            return render_template('profile/change_password.html')
        
        if new_password != confirm_password:
            flash("Passwords do not match", 'danger')
            return render_template('profile/change_password.html')
        
        conn = get_db_connection()
        if not conn:
            flash("Database connection failed", 'danger')
            return render_template('profile/change_password.html')
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password_hash FROM users WHERE user_id = %s", (session['user_id'],))
        user = cursor.fetchone()
        
        # Verify current password
        from utils.auth_utils import verify_password
        if not verify_password(current_password, user['password_hash']):
            cursor.close()
            conn.close()
            flash("Current password is incorrect", 'danger')
            return render_template('profile/change_password.html')
        
        # Hash new password
        new_password_hash = hash_password(new_password)
        
        try:
            cursor.execute("""
                UPDATE users 
                SET password_hash = %s
                WHERE user_id = %s
            """, (new_password_hash, session['user_id']))
            
            conn.commit()
            flash("Password changed successfully!", 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('profile.view_profile'))
            
        except Exception as e:
            conn.rollback()
            flash(f"Error changing password: {str(e)}", 'danger')
            cursor.close()
            conn.close()
            return render_template('profile/change_password.html')
    
    return render_template('profile/change_password.html')