#!/bin/bash
# Pipeline completo de recolección, procesamiento y entrenamiento

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Pipeline SEMMA - Detección de Vulnerabilidades         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Paso 1: Configuración
echo "[1/5] Cargando configuración..."
source ./0_config.sh
echo ""

# Paso 2: Recolección de PoCs
echo "[2/5] Recolectando PoCs de GitHub..."
./1_github_poc.sh
echo ""

# Paso 3: Recolección de exploits
echo "[3/5] Buscando exploits con searchsploit..."
./2_searchsploit.sh || echo "    [!] Searchsploit no disponible, continuando..."
echo ""

# Paso 4: Generación de features
echo "[4/5] Generando dataset y features TF-IDF..."
python3 5_make_features.py
echo ""

# Paso 5: Entrenamiento
echo "[5/5] Entrenando modelo Random Forest..."
python3 6_train_model.py
echo ""

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  ✅ Pipeline completado exitosamente                     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Para analizar un archivo:"
echo "  python3 scripts/7_detect_file.py /ruta/al/archivo.py"
echo ""
