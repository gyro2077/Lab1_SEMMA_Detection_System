def login(login, passwd):
  query = "SELECT * FROM users WHERE user = '" + login + "' AND pass = '" + passwd + "'"
  return db.execute(query)