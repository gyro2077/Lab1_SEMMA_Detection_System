# Python SQL Injection Example
import sqlite3

def get_user_data(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # VULNERABLE: String formatting with user input
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()

def search_products(keyword):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Direct string concatenation
    sql = "SELECT * FROM products WHERE name LIKE '%" + keyword + "%'"
    cursor.execute(sql)
    return cursor.fetchall()

def login(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # VULNERABLE: String interpolation allows OR 1=1
    query = "SELECT * FROM accounts WHERE user='%s' AND pass='%s'" % (username, password)
    cursor.execute(query)
    
    if cursor.fetchone():
        return True
    return False

# Vulnerable API endpoint simulation
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        user_data = get_user_data(sys.argv[1])
        print(user_data)
