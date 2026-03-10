import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        return conn
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def init_db():
    """Initialize database and create all tables"""
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('customer', 'super_admin', 'product_manager', 'order_manager', 'delivery_manager') DEFAULT 'customer',
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                phone VARCHAR(15),
                profile_image VARCHAR(255),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Addresses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS addresses (
                address_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                address_type ENUM('home', 'office', 'other') DEFAULT 'home',
                street_address VARCHAR(255) NOT NULL,
                city VARCHAR(50) NOT NULL,
                state VARCHAR(50) NOT NULL,
                postal_code VARCHAR(10) NOT NULL,
                country VARCHAR(50) DEFAULT 'India',
                phone VARCHAR(15),
                is_default BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        
        # Categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INT AUTO_INCREMENT PRIMARY KEY,
                category_name VARCHAR(100) NOT NULL,
                description TEXT,
                image_url VARCHAR(255),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                category_id INT NOT NULL,
                product_name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                discount_price DECIMAL(10, 2),
                stock_quantity INT DEFAULT 0,
                sku VARCHAR(100) UNIQUE,
                rating DECIMAL(3, 2) DEFAULT 0,
                total_reviews INT DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                created_by INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(category_id),
                FOREIGN KEY (created_by) REFERENCES users(user_id)
            )
        """)
        
        # Product images table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_images (
                image_id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT NOT NULL,
                image_url VARCHAR(255) NOT NULL,
                is_primary BOOLEAN DEFAULT FALSE,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
            )
        """)
        
        # Cart table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                cart_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        
        # Cart items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart_items (
                cart_item_id INT AUTO_INCREMENT PRIMARY KEY,
                cart_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL DEFAULT 1,
                price DECIMAL(10, 2) NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cart_id) REFERENCES cart(cart_id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
            )
        """)
        
        # Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                shipping_address_id INT,
                order_status ENUM('placed', 'payment_verified', 'processing', 'packed', 'shipped', 'out_for_delivery', 'delivered', 'cancelled') DEFAULT 'placed',
                payment_method ENUM('upi', 'card') NOT NULL,
                payment_status ENUM('pending', 'verified', 'failed', 'refunded') DEFAULT 'pending',
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                estimated_delivery DATE,
                delivered_date DATETIME,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (shipping_address_id) REFERENCES addresses(address_id)
            )
        """)
        
        # Order items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10, 2) NOT NULL,
                total_price DECIMAL(10, 2) NOT NULL,
                rating INT,
                feedback TEXT,
                FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)
        
        # Payments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                payment_amount DECIMAL(10, 2) NOT NULL,
                payment_method ENUM('upi', 'card') NOT NULL,
                transaction_id VARCHAR(100),
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                payment_status ENUM('pending', 'success', 'failed') DEFAULT 'pending',
                FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
            )
        """)
        
        # Delivery tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS delivery_tracking (
                tracking_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                status ENUM('order_placed', 'payment_verified', 'processing', 'packed', 'shipped', 'out_for_delivery', 'delivered') DEFAULT 'order_placed',
                location VARCHAR(255),
                status_update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                updated_by INT,
                FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
                FOREIGN KEY (updated_by) REFERENCES users(user_id)
            )
        """)
        
        # Refunds table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS refunds (
                refund_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                refund_amount DECIMAL(10, 2) NOT NULL,
                refund_reason TEXT,
                refund_status ENUM('pending', 'processed', 'completed') DEFAULT 'pending',
                request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_date DATETIME,
                FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
            )
        """)
        
        # Feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                feedback_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_id INT,
                rating INT NOT NULL,
                comment TEXT,
                is_verified_purchase BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        """)
        
        conn.commit()
        print("✅ Database tables created successfully!")
        return True
        
    except Error as e:
        print(f"❌ Error creating tables: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db()