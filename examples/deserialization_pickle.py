# Python pickle deserialization
import pickle

def load_user_data(data):
    # VULNERABLE: Deserializing untrusted data
    user = pickle.loads(data)
    return user
