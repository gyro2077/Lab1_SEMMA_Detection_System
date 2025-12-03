@app.route('/profile')
def profile():
    username = request.args.get('user')
    return f"<h1>Profile: {username}</h1>" 