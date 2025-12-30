"""
Flacon-Cloud Backend API
FastAPI + SQLite для управления каталогом духов
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from pathlib import Path

app = FastAPI(title="Flacon-Cloud API", version="1.0.0")

# CORS - разрешаем запросы отовсюду (для демки норм)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = Path(__file__).parent / "shop.db"


def get_db():
    """Подключение к SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Инициализация базы данных с демо-товарами"""
    conn = get_db()
    c = conn.cursor()
    
    # Для демо: всегда пересоздаем таблицу, чтобы картинки были свежие
    c.execute("DROP TABLE IF EXISTS products")
    
    c.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT NOT NULL,
            price INTEGER NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            description TEXT,
            image TEXT,
            category TEXT DEFAULT 'unisex'
        )
    ''')
    
    # Добавляем лакшери-духи (все картинки .png!)
    demo_products = [
        ("Lost Cherry", "Tom Ford", 45000, 5, "Вишнёвый ликёр с нотами миндаля и корицы", "/images/cherry.png", "unisex"),
        ("Baccarat Rouge 540", "Maison Francis Kurkdjian", 38000, 3, "Легендарный аромат с янтарём и жасмином", "/images/baccarat.png", "unisex"),
        ("Oud Wood", "Tom Ford", 32000, 7, "Благородный уд с нотами сандала и ветивера", "/images/oud.png", "unisex"),
        ("Aventus", "Creed", 55000, 2, "Культовый мужской аромат с ананасом и берёзой", "/images/aventus.png", "male"),
        ("Chanel No 5", "Chanel", 16000, 12, "Вечная классика альдегидов и цветов", "/images/chanel.png", "female"),
    ]
    
    c.executemany(
        "INSERT INTO products (name, brand, price, stock, description, image, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
        demo_products
    )
    conn.commit()
    
    conn.close()


# Инициализируем базу при старте
init_db()


class StockUpdate(BaseModel):
    """Модель для обновления остатков"""
    product_id: int
    change: int  # положительное или отрицательное число


class ProductCreate(BaseModel):
    """Модель для создания товара"""
    name: str
    brand: str
    price: int
    stock: int = 0
    description: str = ""
    image: str = ""
    category: str = "unisex"


@app.get("/")
def root():
    """Health check"""
    return {"status": "ok", "message": "Flacon-Cloud API is running 🌸"}


@app.get("/api/products")
def get_products(search: str = None, category: str = None):
    """
    Получить список всех товаров
    Опционально: фильтр по поиску и категории
    """
    conn = get_db()
    c = conn.cursor()
    
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    
    if search:
        query += " AND (name LIKE ? OR brand LIKE ? OR description LIKE ?)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])
    
    if category and category != "all":
        query += " AND category = ?"
        params.append(category)
    
    query += " ORDER BY brand, name"
    
    c.execute(query, params)
    products = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return products


@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    """Получить один товар по ID"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return {"error": "Product not found"}


@app.post("/api/stock/update")
def update_stock(data: StockUpdate):
    """
    Обновить остаток товара
    change может быть +1 (приёмка) или -1 (продажа)
    """
    conn = get_db()
    c = conn.cursor()
    
    # Обновляем, но не даём уйти в минус
    c.execute(
        "UPDATE products SET stock = MAX(0, stock + ?) WHERE id = ?",
        (data.change, data.product_id)
    )
    conn.commit()
    
    # Возвращаем обновлённый товар
    c.execute("SELECT * FROM products WHERE id = ?", (data.product_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return {"success": True, "product": dict(row)}
    return {"success": False, "error": "Product not found"}


@app.post("/api/products")
def create_product(product: ProductCreate):
    """Добавить новый товар"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        """INSERT INTO products (name, brand, price, stock, description, image, category)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (product.name, product.brand, product.price, product.stock, 
         product.description, product.image, product.category)
    )
    conn.commit()
    product_id = c.lastrowid
    conn.close()
    
    return {"success": True, "id": product_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
