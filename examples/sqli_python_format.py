# Python string formatting SQLi
import sqlite3

def get_user(user_id):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = {}".format(user_id)
    cursor.execute(query)
    return cursor.fetchone()
