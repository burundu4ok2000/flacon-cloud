import sqlite3

DB_PATH = 'backend/shop.db'

def fix_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Update J'adore to Chanel No 5 to match our new authentic image
    print("Converting J'adore to Chanel No 5...")
    c.execute("""
        UPDATE products 
        SET name = 'No 5', 
            brand = 'Chanel', 
            description = 'Легендарный пудровый аромат с нотами альдегидов, розы и жасмина',
            image = '/images/chanel.png'
        WHERE name = 'J''adore' OR name LIKE '%J''adore%'
    """)

    # Update images for others
    updates = [
        ('/images/cherry.png', '%Lost Cherry%'),
        ('/images/baccarat.png', '%Baccarat%'),
        ('/images/oud.png', '%Oud Wood%'),
        ('/images/oud.png', '%Aventus%') # Fallback for Aventus
    ]
    
    for img, name_pattern in updates:
        c.execute("UPDATE products SET image = ? WHERE name LIKE ?", (img, name_pattern))

    conn.commit()
    
    print("\n--- Current Catalog ---")
    c.execute("SELECT id, brand, name, image FROM products")
    for row in c.fetchall():
        print(row)
        
    conn.close()

if __name__ == '__main__':
    fix_data()
