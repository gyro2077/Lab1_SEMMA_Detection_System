# ================================================================
# SEMMA VULNERABILITY DETECTION PIPELINE - WINDOWS VERSION
# PowerShell script para ejecutar todo el flujo en Windows
# ================================================================

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          SEMMA VULNERABILITY DETECTION PIPELINE                ║" -ForegroundColor Cyan
Write-Host "║                    (Windows Version)                           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el entorno virtual
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  No estás en un entorno virtual." -ForegroundColor Yellow
    Write-Host "   Ejecuta: .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "   (Si hay error de ejecución de scripts, ejecuta primero:" -ForegroundColor Yellow
    Write-Host "    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)" -ForegroundColor Yellow
    exit 1
}

$ErrorActionPreference = "Stop"

# PASO 1: Descargar PoCs de GitHub (OPCIONAL - requiere git)
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📥 PASO 1/5: Descargando PoCs de GitHub (opcional)..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "[+] Git detectado. Descargando PoCs..." -ForegroundColor Green
    
    # CVEs a descargar (adaptado de 1_github_poc.sh)
    $CVE_LIST = @(
        "CVE-2020-1472",
        "CVE-2021-3156", 
        "CVE-2021-44228",
        "CVE-2023-38831",
        "CVE-2023-36884"
    )
    
    $POC_DIR = "dataset\github_poc"
    New-Item -ItemType Directory -Force -Path $POC_DIR | Out-Null
    
    foreach ($cve in $CVE_LIST) {
        $search_url = "https://api.github.com/search/repositories?q=$cve+poc&sort=stars&order=desc"
        Write-Host "  Buscando $cve..." -ForegroundColor Gray
        
        try {
            $response = Invoke-RestMethod -Uri $search_url -Headers @{"User-Agent"="PowerShell"}
            if ($response.items.Count -gt 0) {
                $repo_url = $response.items[0].clone_url
                $repo_name = $response.items[0].name
                $target_dir = "$POC_DIR\$cve-$repo_name"
                
                if (-not (Test-Path $target_dir)) {
                    git clone --depth 1 $repo_url $target_dir 2>$null
                    Write-Host "    ✓ Descargado: $repo_name" -ForegroundColor Green
                }
            }
        } catch {
            Write-Host "    ! Error descargando $cve" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "⚠️  Git no instalado. Saltando descarga de PoCs..." -ForegroundColor Yellow
    Write-Host "   (Puedes instalarlo desde: https://git-scm.com/)" -ForegroundColor Gray
}

# PASO 2: Generar ejemplos sintéticos (430 archivos)
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔧 PASO 2/5: Generando 430 ejemplos sintéticos..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

python scripts\3_generate_massive_dataset.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error generando dataset sintético" -ForegroundColor Red
    exit 1
}

# PASO 3: Descargar repositorios REALES (CRÍTICO)
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🌐 PASO 3/5: Descargando repositorios REALES (DVWA, WebGoat, etc)..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

python scripts\4_download_real_datasets.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error descargando datasets reales" -ForegroundColor Red
    exit 1
}

# PASO 4: Generar features (TF-IDF)
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "⚙️  PASO 4/5: Generando features TF-IDF..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

python scripts\5_make_features.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error generando features" -ForegroundColor Red
    exit 1
}

# PASO 5: Entrenar modelo XGBoost
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🤖 PASO 5/5: Entrenando modelo XGBoost..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

python scripts\6_train_model.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error entrenando modelo" -ForegroundColor Red
    exit 1
}

# PASO 6: Prueba del detector
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🧪 Probando detector en archivo de ejemplo..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

if (Test-Path "examples\vulnerable_sqli.php") {
    python scripts\7_detect_file.py examples\vulnerable_sqli.php
} else {
    Write-Host "⚠️  No se encontró archivo de prueba. Usa: python scripts\7_detect_file.py <archivo>" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    ✅ PIPELINE COMPLETADO                      ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Mostrar estadísticas
if (Test-Path "dataset\samples.csv") {
    $lineCount = (Get-Content "dataset\samples.csv" | Measure-Object -Line).Lines
    Write-Host "📊 Dataset generado: $lineCount muestras" -ForegroundColor Cyan
}

Write-Host "🤖 Modelo entrenado: models\model_xgb.pkl" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Para detectar vulnerabilidades:" -ForegroundColor Yellow
Write-Host "   python scripts\7_detect_file.py <archivo>" -ForegroundColor Yellow
Write-Host ""
