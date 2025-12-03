def login(username, pwd):
  query = "SELECT * FROM users WHERE user = '" + username + "' AND pass = '" + pwd + "'"
  return db.execute(query)