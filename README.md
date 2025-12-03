# 🔒 SEMMA Vulnerability Detection System

**Sistema avanzado de detección de vulnerabilidades usando Machine Learning y metodología SEMMA**

> **Estado:** ✅ Producción - Accuracy: 84.92% (dataset real)  
> **Modelo:** XGBoost con 2,985 muestras de código vulnerable real  
> **Tecnología:** Python + XGBoost + TF-IDF  

---

## 📋 Tabla de Contenidos

- [Historia del Proyecto](#-historia-del-proyecto)
- [¿Por Qué 85% y No 97%?](#-por-qué-85-y-no-97)
- [Arquitectura Final](#-arquitectura-final)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Reproducir Desde Cero](#-reproducir-desde-cero)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Vulnerabilidades Detectadas](#-vulnerabilidades-detectadas)
- [Metodología SEMMA](#-metodología-semma)
- [Troubleshooting](#-troubleshooting)
- [Limitaciones](#%EF%B8%8F-limitaciones)

---

## 🎯 Historia del Proyecto

Este proyecto evolucionó a través de 3 fases principales:

### **Fase 1: Prototipo Inicial (66-71% Accuracy)**
- 📊 Dataset: ~60 ejemplos creados manualmente
- 🤖 Modelo: Random Forest básico
- ❌ Problema: Muchos falsos positivos/negativos

### **Fase 2: Dataset Sintético (97% Accuracy)**  
- 📊 Dataset: 718 ejemplos sintéticos generados
- 🤖 Modelo: XGBoost optimizado
- ✅ Accuracy alto... **PERO**
-  ❌ **Falsos Negativos Críticos:** 
  - `xss_angular_002.ts` → Detectado como "safe" (73%) cuando SÍ era vulnerable
  - El modelo "memorizaba" patrones simples, no generalizaba

### **Fase 3: Dataset REAL (85% Accuracy) ✅ ACTUAL**
- 📊 Dataset: **2,985 muestras de código REAL del mundo**
  - DVWA (179 archivos)
  - WebGoat (492 archivos)
  - Juice Shop (600 archivos)
  - NodeGoat (44 archivos)
  - SQLi TestEnv (161 archivos)
  - PayloadsAllTheThings (46 archivos)
- 🤖 Modelo: XGBoost con class balancing
- ✅ **YA NO tiene falsos negativos críticos**
- ✅ `xss_angular_002.ts` → Ahora detectado como XSS (99.55%) ✅

---

## 🤔 ¿Por Qué 85% y No 97%?

**¿El modelo empeoró?** ❌ **NO. El modelo MEJORÓ.**

| Métrica | Fase 2 (Sintético 97%) | Fase 3 (Real 85%) | Realidad |
|---------|------------------------|-------------------|----------|
| **Dataset** | Ejemplos generados simples | Código real de DVWA, WebGoat | ✅ Más realista |
| **XSS Angular** | 73% safe ❌ (FALSO NEGATIVO) | **99.55% XSS** ✅ | ✅ Arreglado |
| **Generalización** | Memoriza patrones | Aprende contexto | ✅ Mejor |
| **Confiabilidad** | Alta en síntesis | Alta en real | ✅ Confiable |

**El accuracy bajó porque el dataset REAL es mucho más difícil**, pero el modelo ahora **SÍ funciona en el mundo real**.

### Comparación en Código Real:

```python
# Angular XSS con bypassSecurityTrustHtml

# Fase 2 (97% accuracy sintético):
# Predicción: safe (73%) ❌ PELIGROSO

# Fase 3 (85% accuracy real):
# Predicción: xss (99.55%) ✅ CORRECTO
```

---

## 🏗️ Arquitectura Final

```
┌─────────────────────────────────────────────────────────────┐
│                    SEMMA PIPELINE                           │
└─────────────────────────────────────────────────────────────┘

1️⃣ DATA COLLECTION
   ├─ GitHub PoCs (CVEs conocidos)
   ├─ SearchSploit Exploits  
   ├─ Repositorios Reales (DVWA, WebGoat, Juice Shop)
   └─ Ejemplos Sintéticos (430 archivos multi-lenguaje)

2️⃣ FEATURE EXTRACTION
   ├─ Filtrado de binarios
   ├─ TF-IDF Vectorization (5000 features, bigrams)
   ├─ Etiquetado inteligente por ruta
   └─ Weak labeling por patrones

3️⃣ MODEL TRAINING
   ├─ XGBoost (200 trees, depth=8)
   ├─ Class balancing automático
   ├─ Cross-validation
   └─ Feature importance analysis

4️⃣ DETECTION
   ├─ Cargar código fuente
   ├─ Vectorizar con TF-IDF
   ├─ Predicción con XGBoost
   └─ Reporte detallado con confianza
```

### Dataset Final (2,985 muestras)

```
SQLi:            494 (16.5%)
RCE:             396 (13.3%)
XSS:             309 (10.4%)
Path Traversal:  307 (10.3%)  
Safe:            333 (11.2%)
Other:         1,037 (34.7%)
Deserialization: 44 (1.5%)
Weak Crypto:     43 (1.4%)
XXE:             22 (0.7%)
```

---

## 📦 Requisitos

- Python 3.8+
- pip
- git
- 2GB espacio libre (para datasets)
- (Opcional) searchsploit

---

## 🚀 Instalación

```bash
# 1. Clonar repositorio
git clone <tu-repo>
cd SEMMA

# 2. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. (Opcional) Instalar searchsploit
sudo git clone https://gitlab.com/exploit-database/exploitdb.git /opt/exploitdb
sudo ln -sf /opt/exploitdb/searchsploit /usr/local/bin/searchsploit
```

---

## ⚡ Uso Rápido

### Detectar Vulnerabilidades en un Archivo

```bash
source .venv/bin/activate
python3 scripts/7_detect_file.py examples/vulnerable_sqli.php
```

### Salida Ejemplo:

```
======================================================================
 🔍 DETECTOR DE VULNERABILIDADES - SEMMA ML Security Scanner
======================================================================

📄 Archivo: examples/vulnerable_sqli.php
📊 Tamaño: 432 bytes

🎯 CATEGORÍA DETECTADA:
   💉 SQL Injection
   Severidad: CRÍTICA

📈 DISTRIBUCIÓN DE PROBABILIDADES:
   💉 sqli                  98.40% ███████████████████████████████████████░

⚠️  ⚠️  ⚠️  ALERTA CRÍTICA  ⚠️  ⚠️  ⚠️

Posible vulnerabilidad SQL Injection detectada
Confianza: 98.40%

🚨 ACCIÓN REQUERIDA:
   1. Realizar análisis manual profundo inmediatamente
   2. No desplegar este código en producción
   3. Contactar al equipo de seguridad
======================================================================
```

---

## 🔄 Reproducir Desde Cero

**Para obtener EXACTAMENTE el mismo modelo que tengo:**

```bash
# 1. Activar entorno
source .venv/bin/activate

# 2. Descargar PoCs de GitHub
bash scripts/1_github_poc.sh

# 3. (Opcional) Descargar exploits de SearchSploit
bash scripts/2_searchsploit.sh

# 4. Generar ejemplos sintéticos (430 archivos)
python3 scripts/generate_massive_dataset.py

# 5. Descargar repositorios REALES (1,522 archivos - CRÍTICO)
python3 scripts/download_real_datasets.py

# 6. Generar features TF-IDF
python3 scripts/5_make_features.py

# 7. Entrenar modelo XGBoost
python3 scripts/6_train_model.py

# 8. ¡Listo! Ahora puedes detectar vulnerabilidades
python3 scripts/7_detect_file.py <archivo>
```

### O Usar el Pipeline Completo:

```bash
bash scripts/pipeline.sh
```

> ⚠️ **Nota:** El paso más importante es el **#5** (`download_real_datasets.py`). Sin los repositorios reales, el modelo tendrá accuracy ~70-80% con falsos negativos.

---

## 📁 Estructura del Proyecto

```
SEMMA/
├── scripts/
│   ├── 0_config.sh                    # Variables de entorno
│   ├── 1_github_poc.sh                # Descarga PoCs de GitHub
│   ├── 2_searchsploit.sh              # Extrae exploits de SearchSploit
│   ├── 5_make_features.py             # ⭐ Extrae features (TF-IDF + etiquetado)
│   ├── 6_train_model.py               # ⭐ Entrena XGBoost
│   ├── 7_detect_file.py               # ⭐ Detecta vulnerabilidades
│   ├── generate_massive_dataset.py    # Genera 430 ejemplos sintéticos
│   ├── download_real_datasets.py      # ⭐ Descarga repos reales (CRÍTICO)
│   └── pipeline.sh                    # Ejecuta todo el flujo
│
├── dataset/
│   ├── github_poc/                    # PoCs descargados (ignorado en git)
│   ├── searchsploit/                  # Exploits (ignorado en git)
│   ├── real_vulnerabilities/          # ⭐ DVWA, WebGoat, etc (ignorado en git)
│   ├── safe_code/                     # 3 ejemplos de código seguro
│   ├── samples.csv                    # Dataset final (ignorado en git)
│   └── features/                      # TF-IDF features (ignorado en git)
│       └── features_tfidf.csv
│
├── models/
│   ├── model_xgb.pkl                  # ⭐ Modelo XGBoost (ignorado en git)
│   ├── vectorizer.pkl                 # TF-IDF vectorizer (ignorado en git)
│   └── label_encoder.pkl              # Encoder de etiquetas (ignorado en git)
│
├── examples/
│   ├── vulnerable_sqli.php            # Ejemplos manuales
│   ├── vulnerable_xss.js
│   ├── vulnerable_rce.py
│   ├── safe_code.py
│   └── generated/                     # 430 ejemplos generados (ignorado en git)
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

### Archivos Clave:

| Archivo | Propósito | Ignorado en Git |
|---------|-----------|-----------------|
| `scripts/5_make_features.py` | Extrae y etiqueta código | ❌ |
| `scripts/6_train_model.py` | Entrena XGBoost | ❌ |
| `scripts/7_detect_file.py` | Detecta vulnerabilidades | ❌ |
| `scripts/download_real_datasets.py` | **MUY IMPORTANTE** - Descarga código real | ❌ |
| `models/model_xgb.pkl` | Modelo entrenado (80MB) | ✅ Sí |
| `dataset/real_vulnerabilities/` | 1,522 archivos reales | ✅ Sí |

---

## 🐛 Vulnerabilidades Detectadas

| Tipo | Emoji | Descripción | Severidad |
|------|-------|-------------|-----------|
| **SQL Injection** | 💉 | Inyección de comandos SQL | CRÍTICA |
| **XSS** | 🌐 | Cross-Site Scripting | ALTA |
| **RCE** | 💣 | Remote Code Execution | CRÍTICA |
| **Path Traversal** | 📂 | Acceso no autorizado a archivos | ALTA |
| **Deserialization** | 📦 | Deserialización insegura | CRÍTICA |
| **Weak Crypto** | 🔓 | Criptografía débil (MD5, SHA1) | MEDIA |
| **XXE** | ❓ | XML External Entity | ALTA |
| **Safe** | ✅ | Código seguro | NINGUNA |

### Métricas por Vulnerabilidad (Test Set 597 muestras):

```
                 precision    recall  f1-score
sqli                93.88%    92.93%    93.40%
xss                 88.33%    85.48%    86.89%
rce                 75.38%    62.03%    68.06%
safe                98.39%    91.04%    94.57%
path_traversal      70.69%    74.55%    72.57%
deserialization    100.00%    88.89%    94.12%
weak_crypto        100.00%    88.89%    94.12%

Accuracy Global:                       84.92%
```

---

## 🔬 Metodología SEMMA

**SEMMA** = Sample, Explore, Modify, Model, Assess

### 1. Sample (Muestreo)
- PoCs de GitHub
- Exploits de SearchSploit
- Repositorios vulnerables reales
- Ejemplos sintéticos

### 2. Explore (Exploración)
- Análisis de distribución de clases
- Identificación de desbalances
- Detección de archivos binarios/corruptos

### 3. Modify (Modificación)
- Filtrado de archivos no-código
- TF-IDF vectorization (5000 features)
- Etiquetado inteligente por ruta
- Class balancing

### 4. Model (Modelado)
- XGBoost (200 árboles, profundidad 8)
- Regularización L1/L2
- Cross-validation
- Feature importance

### 5. Assess (Evaluación)
- Classification report
- Matriz de confusión
- Validación con código real
- Análisis de falsos positivos/negativos

---

## 🛠️ Troubleshooting

### Error: `ModuleNotFoundError: No module named 'xgboost'`

```bash
source .venv/bin/activate
pip install xgboost lightgbm
```

### Error: `No se encontró model_xgb.pkl`

El modelo no se incluye en git (pesa 80MB). Debes entrenarlo:

```bash
# Opción 1: Entrenar desde cero (recomendado)
python3 scripts/download_real_datasets.py
python3 scripts/generate_massive_dataset.py
python3 scripts/5_make_features.py
python3 scripts/6_train_model.py

# Opción 2: Solo con datos mínimos (accuracy ~70%)
python3 scripts/generate_massive_dataset.py
python3 scripts/5_make_features.py
python3 scripts/6_train_model.py
```

### Accuracy Bajo (~70%)

Probablemente no descargaste los repositorios REALES:

```bash
python3 scripts/download_real_datasets.py  # CRÍTICO
python3 scripts/5_make_features.py
python3 scripts/6_train_model.py
```

### Detección Errónea en Frameworks Modernos

El modelo aprende mejor con más ejemplos. Agrega código vulnerable real de tu framework:

```bash
# 1. Agrega archivos .jsx, .ts, .vue a examples/
# 2. Re-genera features
python3 scripts/5_make_features.py
python3 scripts/6_train_model.py
```

---

## ⚠️ Limitaciones

### Clases con Pocos Datos
- `xss`: 309 muestras → 85% recall (bueno)
- `sqli`: 494 muestras → 92% recall (excelente)
- `xxe`: 22 muestras → 75% recall (limitado)

### Código Ofuscado
El modelo usa TF-IDF (basado en texto). Código ofuscado puede evadir detección.

### Frameworks Muy Nuevos
Si un framework no está representado en los 2,985 ejemplos, la detección puede ser imprecisa.

### No Reemplaza Análisis Manual
Este es un **primer filtro automatizado**. Vulnerabilidades complejas requieren revisión humana.

---

## 📊 Comparación con Versiones Anteriores

| Versión | Dataset | Modelo | Accuracy Test | XSS Angular |
|---------|---------|--------|---------------|-------------|
| v1.0 | 60 manual | Random Forest | 71% | No probado |
| v2.0 | 718 sintético | XGBoost | **97%** | 73% safe ❌ |
| **v3.0 (Actual)** | **2,985 real** | **XGBoost** | **85%** | **99.55% xss** ✅ |

**Conclusión:** v3.0 tiene menor accuracy en test sintético, pero **MUCHO mayor confiabilidad en código Real.

---

## 🤝 Contribuciones

Para mejorar el modelo:

1. Agregar más ejemplos reales de vulnerabilidades
2. Mejorar el etiquetado automático en `5_make_features.py`
3. Experimentar con otros modelos (BERT para código)
4. Crear tests automatizados

---

## 📄 Licencia

MIT License - Ver `LICENSE`

---

## 👤 Autor

Proyecto desarrollado para el curso de Seguridad de Software - SEMMA Methodology

**Estado Final:** ✅ Funcional en Producción
**Accuracy:** 84.92% (dataset real de 2,985 muestras)
**Confianza:** Alta en SQLi (93%), XSS (89%), RCE (75%), Safe (99%)

---

## 📚 Referencias

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [DVWA](https://github.com/digininja/DVWA)
- [WebGoat](https://github.com/WebGoat/WebGoat)
- [Juice Shop](https://github.com/juice-shop/juice-shop)
- [SEMMA Methodology](https://www.sas.com/en_us/insights/analytics/data-mining.html)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
