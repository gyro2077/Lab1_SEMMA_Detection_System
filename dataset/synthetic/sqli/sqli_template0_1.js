def login(login, clave):
    q = "SELECT * FROM users WHERE user = '" + login + "' AND pass = '" + clave + "'"
    return db.execute(q)