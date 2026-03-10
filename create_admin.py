from database import get_db_connection
from utils.auth_utils import hash_password

def create_admin_user():
    """Create a super admin user"""
    conn = get_db_connection()
    if not conn:
        print("❌ Database connection failed")
        return
    
    cursor = conn.cursor()
    
    # Admin credentials
    username = 'admin'
    email = 'admin@ecommerce.com'
    password = 'admin123'
    
    try:
        # Check if admin already exists
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            print("⚠️ Admin user already exists!")
            cursor.close()
            conn.close()
            return
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Create super admin
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role, first_name, last_name)
            VALUES (%s, %s, %s, 'super_admin', %s, %s)
        """, (username, email, hashed_password, 'Admin', 'User'))
        
        conn.commit()
        print("✅ Super Admin created successfully!")
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print("\n⚠️ Change this password after first login!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    create_admin_user()