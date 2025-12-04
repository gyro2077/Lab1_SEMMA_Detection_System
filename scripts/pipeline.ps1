# ============================================================================
# SEMMA VULNERABILITY DETECTION PIPELINE - Windows PowerShell
# Ejecuta todo el flujo desde descarga de datos hasta entrenamiento
# ============================================================================

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          SEMMA VULNERABILITY DETECTION PIPELINE                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar entorno virtual
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  No estás en un entorno virtual." -ForegroundColor Yellow
    Write-Host "   Ejecuta: .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    exit 1
}

Set-Location $ProjectRoot

# PASO 1: Descargar PoCs de GitHub
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📥 PASO 1/6: Descargando PoCs de GitHub..." -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# Leer configuración
. "$ProjectRoot\scripts\0_config.sh"

# Crear directorio si no existe
New-Item -ItemType Directory -Force -Path "$ProjectRoot\dataset\github_poc" | Out-Null

# Descargar PoCs (simplificado para Windows)
$CVE_LIST = @(
    "CVE-2021-44228",  # Log4Shell
    "CVE-2023-38831",  # WinRAR RCE
    "CVE-2021-3156",   # Sudo
    "CVE-2020-1472"    # Zerologon
)

foreach ($cve in $CVE_LIST) {
    Write-Host "[+] Buscando PoC para $cve..." -ForegroundColor Green
    # En Windows es complicado hacer búsquedas de GitHub sin script adicional
    # Por ahora lo dejamos como opcional
}

Write-Host "[✓] Descarga de PoCs completada (o saltada)" -ForegroundColor Green

# PASO 2: SearchSploit (opcional - normalmente no está en Windows)
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📥 PASO 2/6: SearchSploit (saltando - no disponible en Windows)" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# PASO 3: Generar ejemplos sintéticos masivos (430 archivos)
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔧 PASO 3/6: Generando 430 ejemplos sintéticos..." -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
python scripts\3_generate_massive_dataset.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "❌ Error generando dataset sintético" -ForegroundColor Red
    exit 1 
}

# PASO 4: Descargar repositorios REALES (CRÍTICO)
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🌐 PASO 4/6: Descargando repositorios REALES (DVWA, WebGoat, etc)..." -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
python scripts\4_download_real_datasets.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "❌ Error descargando datasets reales" -ForegroundColor Red
    exit 1 
}

# PASO 5: Generar features (TF-IDF)
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "⚙️  PASO 5/6: Generando features TF-IDF..." -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
python scripts\5_make_features.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "❌ Error generando features" -ForegroundColor Red
    exit 1 
}

# PASO 6: Entrenar modelo XGBoost
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🤖 PASO 6/6: Entrenando modelo XGBoost..." -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
python scripts\6_train_model.py
if ($LASTEXITCODE -ne 0) { 
    Write-Host "❌ Error entrenando modelo" -ForegroundColor Red
    exit 1 
}

# PASO 7: Prueba del detector
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🧪 PROBANDO: Detector en archivo de ejemplo..." -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# Prueba en un archivo vulnerable
if (Test-Path "examples\vulnerable_sqli.php") {
    python scripts\7_detect_file.py examples\vulnerable_sqli.php
} else {
    Write-Host "⚠️  No se encontró archivo de prueba." -ForegroundColor Yellow
    Write-Host "   Usa: python scripts\7_detect_file.py <archivo>" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    ✅ PIPELINE COMPLETADO                      ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

if (Test-Path "dataset\samples.csv") {
    $lineCount = (Get-Content "dataset\samples.csv" | Measure-Object -Line).Lines
    Write-Host "📊 Dataset generado: $lineCount muestras" -ForegroundColor Cyan
}

Write-Host "🤖 Modelo entrenado: models\model_xgb.pkl" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Para detectar vulnerabilidades:" -ForegroundColor Yellow
Write-Host "   python scripts\7_detect_file.py <archivo>" -ForegroundColor White
Write-Host ""
