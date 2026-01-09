import sqlite3

DATABASE_NAME = "kitaplar.db"

def setup_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kitaplar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT,
        title TEXT NOT NULL,
        author TEXT,
        publisher TEXT,
        price REAL,
        link TEXT
    )
    """)
    conn.commit()
    conn.close()


def insert_book(book):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kitaplar (site, title, author, publisher, price, link)
        VALUES (?,?,?,?,?,?)
    """, (
        book["site"],
        book["title"],
        book["author"],
        book["publisher"],
        book["price"],
        book["link"],
    ))
    conn.commit()
    conn.close()


def get_all_books():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kitaplar ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_book(id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM kitaplar WHERE id=?", (id,))
    conn.commit()
    conn.close()


def update_book(id, price):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE kitaplar SET price=? WHERE id=?", (price, id))
    conn.commit()
    conn.close()
