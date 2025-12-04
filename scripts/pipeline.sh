#!/bin/bash
#
# SEMMA PIPELINE COMPLETO
# Ejecuta todo el flujo desde descarga de datos hasta entrenamiento
#

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          SEMMA VULNERABILITY DETECTION PIPELINE                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar entorno virtual
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  No estás en un entorno virtual."
    echo "   Ejecuta: source .venv/bin/activate"
    exit 1
fi

cd "$PROJECT_ROOT"

# PASO 1: Descargar PoCs de GitHub
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📥 PASO 1/7: Descargando PoCs de GitHub..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
bash scripts/1_github_poc.sh

# PASO 2: (Opcional) Descargar exploits de SearchSploit
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📥 PASO 2/7: Descargando exploits de SearchSploit (opcional)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v searchsploit &> /dev/null; then
    bash scripts/2_searchsploit.sh
else
    echo "⚠️  searchsploit no instalado. Saltando..."
fi

# PASO 3: Generar ejemplos sintéticos masivos (430 archivos)
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 PASO 3/7: Generando 430 ejemplos sintéticos..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 scripts/3_generate_massive_dataset.py

# PASO 4: Descargar repositorios REALES (CRÍTICO)
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 PASO 4/7: Descargando repositorios REALES (DVWA, WebGoat, etc)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 scripts/4_download_real_datasets.py

# PASO 5: Generar features (TF-IDF)
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚙️  PASO 5/7: Generando features TF-IDF..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 scripts/5_make_features.py

# PASO 6: Entrenar modelo XGBoost
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤖 PASO 6/7: Entrenando modelo XGBoost..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 scripts/6_train_model.py

# PASO 7: Prueba del detector
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 PASO 7/7: Probando detector en archivo de ejemplo..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Prueba en un archivo vulnerable
if [ -f "examples/vulnerable_sqli.php" ]; then
    python3 scripts/7_detect_file.py examples/vulnerable_sqli.php
else
    echo "⚠️  No se encontró archivo de prueba. Usa: python3 scripts/7_detect_file.py <archivo>"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ PIPELINE COMPLETADO                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Dataset generado: $(wc -l < dataset/samples.csv 2>/dev/null || echo '?') muestras"
echo "🤖 Modelo entrenado: models/model_xgb.pkl"
echo ""
echo "💡 Para detectar vulnerabilidades:"
echo "   python3 scripts/7_detect_file.py <archivo>"
echo ""
