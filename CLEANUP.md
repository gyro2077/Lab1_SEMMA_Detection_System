# 🧹 PROYECTO LIMPIO Y ORGANIZADO

## ✅ Scripts Organizados (Orden Numérico)

```
scripts/
├── 0_config.sh                     # Configuración inicial
├── 1_github_poc.sh                 # Descarga PoCs de GitHub  
├── 2_searchsploit.sh               # Descarga exploits
├── 3_generate_massive_dataset.py   # ⭐ Genera 430 ejemplos sintéticos
├── 4_download_real_datasets.py     # ⭐ Descarga DVWA, WebGoat, etc
├── 5_make_features.py              # ⭐ Extrae features TF-IDF
├── 6_train_model.py                # ⭐ Entrena modelo XGBoost
├── 7_detect_file.py                # ⭐ Detecta vulnerabilidades
├── pipeline.sh                     # 🐧 Pipeline para Linux/macOS
└── pipeline.ps1                    # 🪟 Pipeline para Windows (NUEVO)
```

## 🗑️ Basura Eliminada

- ❌ `scripts/train_model.py` (viejo)
- ❌ `scripts/predict_file.py` (viejo)  
- ❌ `scripts/generate_dataset.py` (viejo)
- ❌ `models/model_rf.pkl` (viejo modelo Random Forest)
- ❌ `models/model_pipeline.pkl` (viejo)
- ❌ `dataset/synthetic/` (directorio vacío)
- ❌ `examples/limpio.ts` (archivo de prueba)
- ❌ `examples/sucio.ts` (archivo de prueba)
- ❌ `__pycache__/` (cache Python)

## 📁 Archivos que Quedan (Solo lo Necesario)

### Modelos (3 archivos)
```
models/
├── model_xgb.pkl        # Modelo XGBoost entrenado (80MB) - IGNORADO EN GIT
├── vectorizer.pkl       # TF-IDF vectorizer - IGNORADO EN GIT
└── label_encoder.pkl    # Encoder de etiquetas - IGNORADO EN GIT
```

### Scripts (9 archivos)
```
scripts/
├── 0_config.sh          # Variables
├── 1_github_poc.sh      # Descarga PoCs
├── 2_searchsploit.sh    # Descarga exploits
├── 3_generate_massive_dataset.py    # Genera sintéticos
├── 4_download_real_datasets.py      # Descarga REALES (CRÍTICO)
├── 5_make_features.py               # Extrae features
├── 6_train_model.py                 # Entrena modelo
├── 7_detect_file.py                 # Detecta
└── pipeline.sh          # Orquestador
```

### Ejemplos (60 archivos manuales)
```
examples/
├── vulnerable_sqli.php
├── vulnerable_xss.js
├── vulnerable_rce.py
├── safe_code.py
├── [56 ejemplos más...]
└── generated/           # 430 archivos generados - IGNORADOS EN GIT
```

### Datasets (IGNORADOS EN GIT - se regeneran)
```
dataset/
├── github_poc/              # ~19 archivos (se descarga)
├── searchsploit/            # ~12 archivos (se descarga)
├── real_vulnerabilities/    # ~1,522 archivos (se descarga)
├── safe_code/               # 3 archivos (incluidos en repo)
├── samples.csv              # 2,985 filas (se genera)
└── features/
    └── features_tfidf.csv   # 2,985 x 5000 (se genera)
```

## 🎯 Para Clonar y Usar

### Linux / macOS
```bash
# 1. Clonar
git clone <repo>
cd SEMMA

# 2. Instalar
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Generar TODO
bash scripts/pipeline.sh

# 4. Usar
python3 scripts/7_detect_file.py <archivo>
```

### Windows
```powershell
# 1. Clonar
git clone <repo>
cd SEMMA

# 2. Instalar
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Generar TODO
.\scripts\pipeline.ps1

# 4. Usar
python scripts\7_detect_file.py <archivo>
```

## 📊 Tamaños

- **Repo en Git:** ~500KB (sin modelos/datasets)
- **Después de pipeline.sh:** ~2GB
  - models/: ~80MB
  - dataset/real_vulnerabilities/: ~1.5GB
  - dataset/samples.csv: ~50MB
  - examples/generated/: ~20MB

## ✅ Verificación

```bash
# Ver estructura limpia
tree -L 2 -I '.venv|__pycache__|*.pyc'

# Contar scripts (debe ser 9)
ls scripts/*.py scripts/*.sh | wc -l

# Verificar modelos (debe ser 3)
ls models/*.pkl | wc -l
```

## 🚀 Estado Final

- ✅ Scripts numerados en orden lógico
- ✅ Basura eliminada
- ✅ README actualizado
- ✅ .gitignore configurado  
- ✅ Pipeline funcional
- ✅ Proyecto reproducible

**TODO LISTO! 🎉**
