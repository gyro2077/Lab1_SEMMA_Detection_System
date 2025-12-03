# Python os.system() RCE
import os

def ping_host(hostname):
    # VULNERABLE: Command injection
    os.system("ping -c 4 " + hostname)
