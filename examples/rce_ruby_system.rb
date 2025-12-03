# Ruby system() RCE
def backup_file(filename)
  # VULNERABLE: Command injection
  system("tar -czf backup.tar.gz #{filename}")
end
