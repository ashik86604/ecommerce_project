import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Database
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'ecommerce_db'
    
#mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "ashiks.shabbir@gmail.com"
    MAIL_PASSWORD = "etje rlgg zmqx kiuz"
    MAIL_DEFAULT_SENDER = "ashiks.shabbir@gmail.com"

    # File uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads/products')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    
    # Razorpay Configuration
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_SOQbAh2VaZaTAd')
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'hwkrcR1Nf3Q9WWCDGVd7eYR5')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# import os
# from datetime import timedelta

# class Config:
#     """Base configuration"""
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
#     PERMANENT_SESSION_LIFETIME = timedelta(days=7)
#     SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
#     SESSION_COOKIE_HTTPONLY = True
#     SESSION_COOKIE_SAMESITE = 'Lax'
    
#     # Database
#     MYSQL_HOST = 'localhost'
#     MYSQL_USER = 'root'
#     MYSQL_PASSWORD = 'root'
#     MYSQL_DB = 'ecommerce_db'
    
#     # File uploads
#     MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
#     UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads/products')
#     ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# class DevelopmentConfig(Config):
#     """Development configuration"""
#     DEBUG = True
#     TESTING = False

# class ProductionConfig(Config):
#     """Production configuration"""
#     DEBUG = False
#     TESTING = False
#     SESSION_COOKIE_SECURE = True

# class TestingConfig(Config):
#     """Testing configuration"""
#     DEBUG = True
#     TESTING = True

# config = {
#     'development': DevelopmentConfig,
#     'production': ProductionConfig,
#     'testing': TestingConfig,
#     'default': DevelopmentConfig
# }
# import os
# from datetime import timedelta

# class Config:
#     """Base configuration"""
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
#     PERMANENT_SESSION_LIFETIME = timedelta(days=7)
#     SESSION_COOKIE_SECURE = False
#     SESSION_COOKIE_HTTPONLY = True
#     SESSION_COOKIE_SAMESITE = 'Lax'
    
#     # Database
#     MYSQL_HOST = 'localhost'
#     MYSQL_USER = 'root'
#     MYSQL_PASSWORD = 'root'
#     MYSQL_DB = 'ecommerce_db'
    
#     # Razorpay Payment Gateway
#     RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID') or 'rzp_test_SNuINeethx6QXz'
#     RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET') or '4mI4tNr8napACzw0xTyJXWym'
    
#     # File uploads
#     MAX_CONTENT_LENGTH = 16 * 1024 * 1024
#     UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads/products')
#     ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}