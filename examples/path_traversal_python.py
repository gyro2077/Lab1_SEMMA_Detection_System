# Path Traversal example 1
import os

def read_file(filename):
    # VULNERABLE: No path validation
    file_path = "/var/www/uploads/" + filename
    with open(file_path, 'r') as f:
        return f.read()

# Attack: filename = "../../etc/passwd"
