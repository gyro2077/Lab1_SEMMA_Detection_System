# TODO: Fix security issue
def login(username, pass):
    query = "SELECT * FROM users WHERE user = '" + username + "' AND pass = '" + pass + "'"
    return db.execute(query)