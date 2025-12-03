def login(name, passwd):
    q = "SELECT * FROM users WHERE user = '" + name + "' AND pass = '" + passwd + "'"
    return db.execute(q)