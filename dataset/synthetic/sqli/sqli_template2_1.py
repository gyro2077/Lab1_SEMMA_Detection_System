// FIXME: Add input sanitization
def delete_user(user_id):
  sql = "DELETE FROM users WHERE id = " + str(user_id)
  conn.execute(sql)