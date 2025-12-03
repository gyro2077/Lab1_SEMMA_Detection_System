#!/bin/bash
# Extrae exploits de searchsploit (si está instalado)

set -e

# Cargar configuración
source "$(dirname "$0")/0_config.sh"

mkdir -p "$SEARCHSPLOIT_DIR"

echo "[+] Buscando exploits con searchsploit..."

# Verificar si searchsploit está instalado
if ! command -v searchsploit &> /dev/null; then
    echo "[!] searchsploit no está instalado."
    echo "    Para instalarlo: sudo apt install exploitdb"
    echo "    Continuando sin esta fuente de datos..."
    exit 0
fi

# Buscar exploits para CVEs específicos
for cve in "${CVES[@]}"; do
    echo "  [*] Buscando: $cve"
    
    # Crear directorio para este CVE
    cve_dir="$SEARCHSPLOIT_DIR/$cve"
    mkdir -p "$cve_dir"
    
    # Buscar y copiar exploits
    searchsploit -w "$cve" > "$cve_dir/searchsploit_results.txt" 2>/dev/null || true
    
    # Intentar copiar exploits (esto requiere conocer la ruta de exploitdb)
    if [ -d "/usr/share/exploitdb" ]; then
        # Extraer paths y copiar
        searchsploit -m "$cve" -p 2>/dev/null | grep "Exploit:" | awk '{print $2}' | while read -r exploit_path; do
            if [ -f "$exploit_path" ]; then
                cp "$exploit_path" "$cve_dir/" 2>/dev/null || true
            fi
        done
    fi
done

# Buscar exploits por palabras clave
echo "[+] Buscando por palabras clave..."
for keyword in "sql injection" "xss" "rce" "command injection"; do
    keyword_safe=$(echo "$keyword" | tr ' ' '_')
    keyword_dir="$SEARCHSPLOIT_DIR/keyword_$keyword_safe"
    mkdir -p "$keyword_dir"
    
    # Guardar solo listado (para no saturar)
    searchsploit "$keyword" -w 2>/dev/null | head -20 > "$keyword_dir/results.txt" || true
done

# Contar archivos
total_files=$(find "$SEARCHSPLOIT_DIR" -type f | wc -l)
echo "[+] Total de archivos en searchsploit: $total_files"

echo "[✓] Búsqueda en searchsploit completada"
