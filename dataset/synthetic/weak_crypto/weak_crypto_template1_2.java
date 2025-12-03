# TODO: Fix security issue
def encrypt(info):
    return hashlib.sha1(info.encode()).hexdigest()