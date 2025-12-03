#!/bin/bash
# Descarga PoCs de GitHub para CVEs conocidos

set -e

# Cargar configuración
source "$(dirname "$0")/0_config.sh"

mkdir -p "$GITHUB_POC_DIR"

echo "[+] Recolectando PoCs de GitHub..."

# Función para clonar o actualizar repo
clone_or_update() {
    local url=$1
    local target_dir=$2
    
    if [ -d "$target_dir/.git" ]; then
        echo "    [*] Actualizando: $target_dir"
        (cd "$target_dir" && git pull -q)
    else
        echo "    [+] Clonando: $url"
        git clone -q "$url" "$target_dir" 2>/dev/null || true
    fi
}

# PoCs conocidos de GitHub (puedes agregar más)
declare -A POC_REPOS=(
    ["CVE-2023-38831"]="https://github.com/d47d3v1lr/CVE-2023-38831"
    ["CVE-2023-36884"]="https://github.com/Xnuvers007/CVE-2023-36884"
    ["CVE-2021-44228"]="https://github.com/kozmer/log4j-shell-poc"
    ["CVE-2021-3156"]="https://github.com/blasty/CVE-2021-3156"
    ["CVE-2020-1472"]="https://github.com/dirkjanm/CVE-2020-1472"
)

# Clonar repositorios
for cve in "${!POC_REPOS[@]}"; do
    url="${POC_REPOS[$cve]}"
    target="$GITHUB_POC_DIR/$cve"
    clone_or_update "$url" "$target"
done

# Contar archivos recolectados
total_files=$(find "$GITHUB_POC_DIR" -type f | wc -l)
echo "[+] Total de archivos en github_poc: $total_files"

echo "[✓] Recolección de PoCs completada"
