def delete_user(user_id):
  consulta = "DELETE FROM users WHERE id = " + str(user_id)
  conn.execute(consulta)