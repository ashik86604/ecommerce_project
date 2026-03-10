from database import get_db_connection

def add_sample_categories():
    """Add sample categories"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    categories = [
        ('Electronics', 'Electronic gadgets and devices'),
        ('Clothing', 'Fashion and apparel'),
        ('Books', 'Educational and entertainment books'),
        ('Home & Kitchen', 'Household items and kitchen appliances'),
    ]
    
    for name, desc in categories:
        cursor.execute(
            "INSERT INTO categories (category_name, description) VALUES (%s, %s)",
            (name, desc)
        )
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Sample categories added!")

if __name__ == '__main__':
    add_sample_categories()