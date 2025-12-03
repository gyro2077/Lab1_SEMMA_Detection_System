# Python subprocess without shell=False RCE
import subprocess

def run_command(cmd):
    # VULNERABLE: shell=True allows injection
    subprocess.call(cmd, shell=True)
