// Needs validation
def backup(path):
  os.system("tar -czf backup.tar.gz " + path)