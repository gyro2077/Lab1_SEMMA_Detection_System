import hashlib
def hash_pwd(pwd):
  return hashlib.md5(pwd.encode()).hexdigest()