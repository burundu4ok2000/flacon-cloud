import sqlite3
import os

DB_PATH = 'backend/shop.db'

def update_images():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Mapping: (Name part, New Image Path)
    updates = [
        ('Lost Cherry', '/images/cherry.png'),
        ('Baccarat', '/images/baccarat.png'),
        ('Oud Wood', '/images/oud.png'),
        ('J\'adore', '/images/classic.png'),
        ('Aventus', '/images/oud.png') # Reuse dark logic for now
    ]
    
    for name_part, img_path in updates:
        print(f"Updating {name_part} -> {img_path}")
        c.execute("UPDATE products SET image = ? WHERE name LIKE ?", (img_path, f"%{name_part}%"))
        
    conn.commit()
    print("Updates committed.")
    
    # Verify
    c.execute("SELECT name, image FROM products")
    for row in c.fetchall():
        print(row)
        
    conn.close()

if __name__ == '__main__':
    update_images()
