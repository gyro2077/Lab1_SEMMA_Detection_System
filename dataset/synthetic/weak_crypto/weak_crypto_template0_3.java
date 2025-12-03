import hashlib
def hash_passwd(passwd):
  return hashlib.md5(passwd.encode()).hexdigest()