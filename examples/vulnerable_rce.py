#!/usr/bin/env python3
# Ejemplo de código vulnerable a RCE (Remote Code Execution)

import os
import subprocess

def backup_file(filename):
    # Vulnerable: comando del sistema sin validación
    os.system(f"cp {filename} /backup/")

def process_image(image_path):
    # Vulnerable: ejecución de comando con input del usuario
    cmd = f"convert {image_path} -resize 800x600 output.jpg"
    subprocess.call(cmd, shell=True)

def run_script(script_name):
    # Vulnerable: ejecución directa de código
    exec(open(script_name).read())
