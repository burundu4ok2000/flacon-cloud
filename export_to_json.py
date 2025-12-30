import sqlite3
import json
import os

DB_PATH = 'backend/shop.db'
OUTPUT_PATH = 'public/products.json'

def export_db_to_json():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM products ORDER BY brand, name")
    rows = c.fetchall()
    
    products = [dict(row) for row in rows]
    
    # Save to public folder so Astro can serve it statically
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Exported {len(products)} products to {OUTPUT_PATH}")
    conn.close()

if __name__ == '__main__':
    export_db_to_json()
