from flask import Blueprint, app, render_template, request, redirect, url_for, session, flash
from database import get_db_connection
from utils.auth_utils import hash_password, verify_password
import re
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flask_mail import Mail
mail = Mail()
serializer = URLSafeTimedSerializer("your_secret_key")

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append("Username must be at least 3 characters")
        
        if not email or not is_valid_email(email):
            errors.append("Invalid email address")
        
        if not password or len(password) < 6:
            errors.append("Password must be at least 6 characters")
        
        if password != confirm_password:
            errors.append("Passwords do not match")
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html')
        
        # Check if user exists
        conn = get_db_connection()
        if not conn:
            flash("Database connection failed", 'danger')
            return render_template('register.html')
        
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email = %s OR username = %s", (email, username))
        
        if cursor.fetchone():
            flash("Username or email already exists", 'danger')
            cursor.close()
            conn.close()
            return render_template('register.html')
        
        # Create user
        try:
            hashed_password = hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role, first_name, last_name)
                VALUES (%s, %s, %s, 'customer', %s, %s)
            """, (username, email, hashed_password, first_name, last_name))
            
            conn.commit()
            flash("Registration successful! Please login.", 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            conn.rollback()
            flash(f"Registration failed: {str(e)}", 'danger')
            cursor.close()
            conn.close()
            return render_template('register.html')
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash("Email and password required", 'danger')
            return render_template('login.html')
        
        conn = get_db_connection()
        if not conn:
            flash("Database connection failed", 'danger')
            return render_template('login.html')
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, username, email, password_hash, role FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and verify_password(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['role'] = user['role']
            session.permanent = True
            
            flash(f"Welcome, {user['username']}!", 'success')
            
            # Redirect based on role
            if user['role'] == 'customer':
                return redirect(url_for('index'))  # Changed from 'index' to correct route
            else:
                return redirect(url_for('admin.dashboard'))
        
        flash("Invalid email or password", 'danger')
        return render_template('login.html')
    
    return render_template('login.html')

@auth_bp.route('/forgot-password', methods=['GET','POST'])
def forgot_password():

    if request.method == 'POST':

        email = request.form.get('email')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            flash("Email not found", "danger")
            return render_template("forgot_password.html")

        token = serializer.dumps(email, salt='password-reset')

        reset_link = url_for(
            'auth.reset_password',
            token=token,
            _external=True
        )

        msg = Message(
            subject="Password Reset Request",
            recipients=[email]
        )

        msg.body = f"""
Hello,

Click the link below to reset your password:

{reset_link}

This link expires in 1 hour.
"""

        mail.send(msg)

        flash("Password reset link sent to your email.", "success")

        return redirect(url_for('auth.login'))

    return render_template("forgot_password.html")

@auth_bp.route('/reset-password/<token>', methods=['GET','POST'])
def reset_password(token):

    try:
        email = serializer.loads(
            token,
            salt='password-reset',
            max_age=3600
        )

    except:
        flash("Reset link expired or invalid", "danger")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':

        password = request.form.get('password')

        password_hash = hash_password(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
        "UPDATE users SET password_hash=%s WHERE email=%s",
        (password_hash,email)
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Password updated successfully!", "success")

        return redirect(url_for('auth.login'))

    return render_template("reset_password.html")

@auth_bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash("You have been logged out", 'success')
    return redirect(url_for('auth.login'))