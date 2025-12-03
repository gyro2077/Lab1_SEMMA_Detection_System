# Python % formatting SQLi
import pymysql

def login(username, password):
    conn = pymysql.connect(host='localhost', user='root', db='app')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE user='%s' AND pass='%s'" % (username, password)
    cursor.execute(query)
    return cursor.fetchone() is not None
