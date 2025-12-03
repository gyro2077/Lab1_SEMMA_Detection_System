# Weak cryptography - MD5
import hashlib

def hash_password(password):
    # VULNERABLE: Using weak MD5 algorithm
    return hashlib.md5(password.encode()).hexdigest()

def encrypt_data(data, key):
    # VULNERABLE: Using DES (weak cipher)
    from Crypto.Cipher import DES
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(data)
