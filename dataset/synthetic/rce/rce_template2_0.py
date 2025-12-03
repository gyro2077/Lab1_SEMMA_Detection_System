# TODO: Fix security issue
def backup(path):
    os.system("tar -czf backup.tar.gz " + path)