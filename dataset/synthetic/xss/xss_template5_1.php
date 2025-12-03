@app.route('/profile')
def profile():
  usuario = request.args.get('user')
  return f"<h1>Profile: {usuario}</h1>" 