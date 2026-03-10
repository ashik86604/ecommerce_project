import os
from flask import Flask, render_template
from config import config
from database import init_db


def create_app(config_name='development'):
    # Get the absolute path to the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Create Flask app with correct template folder
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, 'templates'),
        static_folder=os.path.join(project_root, 'static')
    )
    
    # Load config
    app.config.from_object(config[config_name])
    from routes.auth_routes import auth_bp, mail

    mail.init_app(app)
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize database
    try:
        init_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
    
    from routes.auth_routes import auth_bp
    from routes.product_routes import product_bp
    from routes.cart_routes import cart_bp
    from routes.order_routes import order_bp
    from routes.admin_routes import admin_bp
    from routes.address_routes import address_bp
    from routes.profile_routes import profile_bp  # ADD THIS
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(address_bp)
    app.register_blueprint(profile_bp)  # ADD THIS
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('index.html'), 404
    
    @app.errorhandler(403)
    def forbidden(e):
        return "Access Forbidden", 403
    
    return app

# if __name__ == '__main__':
#     app = create_app('development')
#     app.run(debug=True)

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, port=5001)  # Change port number