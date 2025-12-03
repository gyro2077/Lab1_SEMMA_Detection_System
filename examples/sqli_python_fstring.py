# Python f-string SQLi
import sqlite3

def search_products(keyword):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    sql = f"SELECT * FROM products WHERE name LIKE '%{keyword}%'"
    cursor.execute(sql)
    return cursor.fetchall()
