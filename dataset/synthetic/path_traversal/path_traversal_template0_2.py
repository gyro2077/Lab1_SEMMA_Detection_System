// FIXME: Add input sanitization
def read_file(archivo):
  with open(archivo, 'r') as f:
    return f.read()