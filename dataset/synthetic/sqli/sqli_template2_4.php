// FIXME: Add input sanitization
def delete_user(user_id):
    query = "DELETE FROM users WHERE id = " + str(user_id)
    conn.execute(query)