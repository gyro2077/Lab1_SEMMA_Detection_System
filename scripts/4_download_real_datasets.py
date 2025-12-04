#!/usr/bin/env python3
"""
DESCARGADOR DE DATASETS REALES
Descarga código vulnerable real de repositorios conocidos
"""

import os
import subprocess
import sys

# Directorio base
DATASET_DIR = "/home/gyro/Documents/OCT25-MAR26/SOFT_SEGURO/PARCIAL_DOS/4Diciembre/SEMMA/dataset"
REAL_VULNS_DIR = os.path.join(DATASET_DIR, "real_vulnerabilities")
os.makedirs(REAL_VULNS_DIR, exist_ok=True)

# Repositorios conocidos con vulnerabilidades REALES
VULNERABLE_REPOS = [
    # XSS vulnerabilities
    {
        "name": "XSS-Real-World",
        "url": "https://github.com/s0md3v/AwesomeXSS.git",
        "path": "xss_awesome"
    },
    # SQL Injection examples
    {
        "name": "SQLi-Real",
        "url": "https://github.com/sqlmapproject/testenv.git",
        "path": "sqli_testenv"
    },
    # DVWA - Damn Vulnerable Web Application
    {
        "name": "DVWA",
        "url": "https://github.com/digininja/DVWA.git",
        "path": "dvwa"
    },
    # NodeGoat - Vulnerable Node.js app
    {
        "name": "NodeGoat",
        "url": "https://github.com/OWASP/NodeGoat.git",
        "path": "nodegoat"
    },
    # WebGoat - OWASP vulnerable app
    {
        "name": "WebGoat",
        "url": "https://github.com/WebGoat/WebGoat.git",
        "path": "webgoat",
        "depth": 1  # Solo última versión
    },
    # Juice Shop - Modern vulnerable app
    {
        "name": "JuiceShop",
        "url": "https://github.com/juice-shop/juice-shop.git",
        "path": "juice_shop",
        "depth": 1
    },
    # PHP Security vulnerabilities
    {
        "name": "PHP-Vuln",
        "url": "https://github.com/incredibleindishell/PHP-Vulnerability-Code-With-payloads.git",
        "path": "php_vulns"
    },
    # RCE examples
    {
        "name": "RCE-Examples",
        "url": "https://github.com/swisskyrepo/PayloadsAllTheThings.git",
        "path": "payloads_all",
        "depth": 1
    }
]

def clone_repo(repo_info):
    """Clona o actualiza un repositorio"""
    name = repo_info["name"]
    url = repo_info["url"]
    path = os.path.join(REAL_VULNS_DIR, repo_info["path"])
    depth = repo_info.get("depth", None)
    
    if os.path.exists(path):
        print(f"[*] Actualizando {name}...")
        try:
            subprocess.run(["git", "-C", path, "pull"], 
                         check=True, capture_output=True, timeout=60)
            print(f"[+] {name} actualizado")
        except Exception as e:
            print(f"[!] Error actualizando {name}: {e}")
    else:
        print(f"[+] Clonando {name}...")
        try:
            cmd = ["git", "clone"]
            if depth:
                cmd.extend(["--depth", str(depth)])
            cmd.extend([url, path])
            
            subprocess.run(cmd, check=True, capture_output=True, timeout=300)
            print(f"[+] {name} clonado exitosamente")
        except subprocess.TimeoutExpired:
            print(f"[!] Timeout clonando {name} (demasiado grande)")
        except Exception as e:
            print(f"[!] Error clonando {name}: {e}")
    
    return path

def count_files(directory, extensions):
    """Cuenta archivos con extensiones específicas"""
    count = 0
    for root, dirs, files in os.walk(directory):
        # Ignorar carpetas de dependencias
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'vendor', 'target', 'build']]
        
        for f in files:
            if any(f.endswith(ext) for ext in extensions):
                count += 1
    return count

print("="*70)
print("  DESCARGANDO DATASETS REALES DE VULNERABILIDADES")
print("="*70)
print()

total_downloaded = 0
code_extensions = ['.py', '.php', '.js', '.java', '.ts', '.jsx', '.vue', '.rb', '.go']

for repo in VULNERABLE_REPOS:
    print(f"\n--- {repo['name']} ---")
    path = clone_repo(repo)
    
    if os.path.exists(path):
        file_count = count_files(path, code_extensions)
        print(f"    Archivos de código encontrados: {file_count}")
        total_downloaded += file_count

print("\n" + "="*70)
print(f"✅ DESCARGA COMPLETADA")
print(f"📁 Total de archivos de código: {total_downloaded}")
print(f"📂 Ubicación: {REAL_VULNS_DIR}")
print()
print("SIGUIENTE PASO:")
print("  1. Revisar manualmente algunos archivos")
print("  2. Ejecutar: python3 scripts/5_make_features.py")
print("  3. Re-entrenar: python3 scripts/6_train_model.py")
print("="*70)
