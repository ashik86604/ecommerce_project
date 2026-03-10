from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, redirect, url_for, abort

def hash_password(password):
    """Hash a password using Werkzeug"""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

def verify_password(hashed_password, password):
    """Verify a password against its hash"""
    return check_password_hash(hashed_password, password)

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))
            
            if session.get('role') not in allowed_roles:
                abort(403)  # Forbidden
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator