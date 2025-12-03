def delete_user(user_id):
  q = "DELETE FROM users WHERE id = " + str(user_id)
  conn.execute(q)