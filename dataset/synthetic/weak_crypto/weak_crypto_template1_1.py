def encrypt(content):
    return hashlib.sha1(content.encode()).hexdigest()