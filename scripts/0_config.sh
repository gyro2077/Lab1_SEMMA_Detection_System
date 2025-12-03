#!/bin/bash
# Configuración global para scripts de recolección de datos

# Directorios base
export ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export DATASET_DIR="$ROOT_DIR/dataset"
export GITHUB_POC_DIR="$DATASET_DIR/github_poc"
export SEARCHSPLOIT_DIR="$DATASET_DIR/searchsploit"
export SAFE_CODE_DIR="$DATASET_DIR/safe_code"
export MODELS_DIR="$ROOT_DIR/models"

# CVEs de interés para recolección (puedes agregar más)
export CVES=(
    "CVE-2023-38831"
    "CVE-2023-36884"
    "CVE-2023-21608"
    "CVE-2022-26134"
    "CVE-2021-44228"  # Log4Shell
    "CVE-2021-3156"   # Sudo Baron Samedit
    "CVE-2020-1472"   # Zerologon
    "CVE-2019-0708"   # BlueKeep
)

# Palabras clave para búsqueda de PoCs
export POC_KEYWORDS=(
    "SQL Injection"
    "XSS exploit"
    "Remote Code Execution"
    "Command Injection"
    "Path Traversal"
    "Deserialization"
)

echo "[+] Configuración cargada"
echo "    ROOT_DIR: $ROOT_DIR"
echo "    DATASET_DIR: $DATASET_DIR"
