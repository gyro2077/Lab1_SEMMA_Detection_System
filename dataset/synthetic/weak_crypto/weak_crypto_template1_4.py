def encrypt(data):
  return hashlib.sha1(data.encode()).hexdigest()