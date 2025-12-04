#!/usr/bin/env python3
"""
EXTRACTOR DE FEATURES V2 - Con datos REALES
Lee código de datasets reales y aplica etiquetado inteligente
"""

import os
import glob
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# === Rutas base ===
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASET_DIR = os.path.join(ROOT_DIR, "dataset")
GITHUB_POC_DIR = os.path.join(DATASET_DIR, "github_poc")
SEARCHSPLOIT_DIR = os.path.join(DATASET_DIR, "searchsploit")
SAFE_CODE_DIR = os.path.join(DATASET_DIR, "safe_code")
EXAMPLES_DIR = os.path.join(ROOT_DIR, "examples")
REAL_VULNS_DIR = os.path.join(DATASET_DIR, "real_vulnerabilities")  # NUEVO

FEATURES_DIR = os.path.join(DATASET_DIR, "features")
MODELS_DIR = os.path.join(ROOT_DIR, "models")

os.makedirs(FEATURES_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Extensiones de archivos de código válidos
VALID_CODE_EXTENSIONS = {
    '.py', '.js', '.php', '.java', '.c', '.cpp', '.h', '.hpp',
    '.rb', '.go', '.rs', '.sh', '.bash', '.pl', '.r', '.sql',
    '.html', '.htm', '.xml', '.json', '.yaml', '.yml',
    '.md', '.txt', '.cs', '.swift', '.kt', '.scala', '.ts', '.jsx', '.vue'
}

# Mapeo manual CVE -> tipo principal de vulnerabilidad
CVE_TYPE_MAP = {
    "CVE-2020-1472": "rce",
    "CVE-2021-3156": "rce",
    "CVE-2021-44228": "rce",
    "CVE-2023-38831": "rce",
    "CVE-2023-36884": "rce",
    "CVE-2019-0708": "rce",
}

# NUEVO: Mapeo de directorios de repos reales -> etiquetas
REPO_LABEL_MAP = {
    "dvwa": {
        "sqli": ["sql_injection", "sqli"],
        "xss": ["xss", "dom", "reflected", "stored"],
        "rce": ["command_injection", "exec"],
        "path_traversal": ["file_inclusion"],
        "weak_crypto": ["weak_id"]
    },
    "nodegoat": {
        "sqli": ["a1-injection"],
        "xss": ["a7-xss"],
        "rce": ["a1-injection"],
        "deserialization": ["a8-insecure-deser"],
        "weak_crypto": ["a3-sensitive"]
    },
    "webgoat": {
        "sqli": ["SqlInjection", "sql-injection"],
        "xss": ["CrossSiteScripting", "xss"],
        "rce": ["CommandInjection"],
        "path_traversal": ["PathTraversal"],
        "xxe": ["XXE"]
    },
    "juice_shop": {
        "sqli": ["sqli"],
        "xss": ["xss"],
        "rce": ["rce"],
        "xxe": ["xxe"]
    },
    "sqli_testenv": {
        "sqli": [""]  # Todo es SQLi
    },
    "payloads_all": {
        "sqli": ["SQL Injection"],
        "xss": ["XSS", "Cross Site Scripting"],
        "rce": ["Command Injection", "Code Injection"],
        "deserialization": ["Deserialization"],
        "path_traversal": ["Path Traversal", "File Inclusion"]
    }
}

def is_binary_file(filepath):
    """Detecta si un archivo es binario"""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:
                return True
            try:
                chunk.decode('utf-8')
                return False
            except:
                try:
                    chunk.decode('latin-1')
                    return False
                except:
                    return True
    except:
        return True

def is_valid_code_file(filepath):
    """Verifica si un archivo es código válido"""
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in VALID_CODE_EXTENSIONS and ext != '':
        return False
    
    try:
        size = os.path.getsize(filepath)
        if size > 1024 * 1024:
            return False
        if size == 0:
            return False
    except:
        return False
    
    if is_binary_file(filepath):
        return False
    
    return True

def extract_cve_from_path(path: str) -> str | None:
    """Extrae CVE desde la ruta del archivo"""
    m = re.search(r"CVE-\d{4}-\d+", path, re.IGNORECASE)
    if m:
        return m.group(0).upper()
    return None

def label_from_repo_path(filepath: str) -> str | None:
    """
    Determina la etiqueta basándose en la ruta del archivo en repos reales
    """
    # Normalizar path
    filepath = filepath.lower().replace("\\", "/")
    
    # Buscar en qué repo está
    for repo_name, label_patterns in REPO_LABEL_MAP.items():
        if repo_name in filepath:
            # Buscar patrones específicos en el path
            for label, patterns in label_patterns.items():
                for pattern in patterns:
                    if pattern and pattern.lower() in filepath:
                        return label
            
            # Si no encontró patrón específico pero está en repo de una sola categoría
            if repo_name == "sqli_testenv":
                return "sqli"
            
            # Por defecto, intentar extraer de nombre de archivo
            filename = os.path.basename(filepath).lower()
            if any(p in filename for p in ["sqli", "sql_injection", "sql-inject"]):
                return "sqli"
            elif any(p in filename for p in ["xss", "cross-site"]):
                return "xss"
            elif any(p in filename for p in ["rce", "exec", "command"]):
                return "rce"
    
    return None

def weak_label(text: str) -> str:
    """Asigna etiquetas débiles según patrones típicos"""
    t = text.lower()

    # SQL Injection
    if re.search(r"(select\s+.+\s+from|union\s+select|or\s+1=1|information_schema)", t):
        return "sqli"

    # XSS
    if re.search(r"(<script|onerror=|onload=|document\.cookie|innerhtml|dangerouslysetinnerhtml|bypasssecuritytrust)", t):
        return "xss"

    # RCE / Command injection
    if re.search(r"(system\(|exec\(|popen\(|runtime\.getruntime\(\)|processbuilder|shell_exec|`.+`|subprocess\.call.*shell=true)", t):
        return "rce"

    # Path traversal
    if re.search(r"(\.\./|\.\.\\|/etc/passwd|c:\\\\windows\\\\|file_get_contents.*\$)", t):
        return "path_traversal"

    # Deserialización insegura
    if re.search(r"(objectinputstream|readobject\(|pickle\.loads|yaml\.load\(|unserialize\()", t):
        return "deserialization"

    # Cripto débil
    if re.search(r"(md5\(|sha1\(|des_crypt|rc4|cipher\.getinstance\(\"des)", t):
        return "weak_crypto"

    return "other_vuln"

def read_text_files(base_dir: str, source: str, mode: str) -> list[dict]:
    """
    Lee archivos de texto desde base_dir
    mode:
      - "vuln": etiqueta con weak_label + CVE_TYPE_MAP
      - "safe": etiqueta como 'safe'
      - "real_vuln": usa label_from_repo_path primero, luego weak_label
    """
    rows: list[dict] = []
    if not os.path.isdir(base_dir):
        print(f"[!] Directorio no encontrado, se omite: {base_dir}")
        return rows

    skipped_binary = 0
    skipped_invalid = 0
    labeled_by_path = 0

    for path in glob.glob(base_dir + "/**/*", recursive=True):
        if not os.path.isfile(path):
            continue
        
        if not is_valid_code_file(path):
            if is_binary_file(path):
                skipped_binary += 1
            else:
                skipped_invalid += 1
            continue
            
        try:
            with open(path, "r", errors="ignore") as f:
                text = f.read()
        except Exception:
            continue

        if not text.strip():
            continue

        rel_path = os.path.relpath(path, ROOT_DIR)
        cve = extract_cve_from_path(path)

        if mode == "safe":
            label = "safe"
        elif mode == "real_vuln":
            # NUEVO: Intentar etiquetar por ruta del repo primero
            label = label_from_repo_path(rel_path)
            if label:
                labeled_by_path += 1
            else:
                # Fallback a weak_label
                label = weak_label(text)
            
            # Si tenemos CVE, sobreescribir
            if cve and cve in CVE_TYPE_MAP:
                label = CVE_TYPE_MAP[cve]
        else:  # mode == "vuln"
            label = weak_label(text)
            if cve and cve in CVE_TYPE_MAP:
                label = CVE_TYPE_MAP[cve]

        rows.append({
            "source": source,
            "file_path": rel_path,
            "cve": cve,
            "code": text,
            "label": label,
        })
    
    if skipped_binary > 0:
        print(f"  [i] Archivos binarios filtrados: {skipped_binary}")
    if skipped_invalid > 0:
        print(f"  [i] Archivos no-código filtrados: {skipped_invalid}")
    if mode == "real_vuln" and labeled_by_path > 0:
        print(f"  [+] Etiquetados por ruta: {labeled_by_path}")
    
    return rows

def read_examples() -> list[dict]:
    """Integra ejemplos de ../examples"""
    rows: list[dict] = []
    if not os.path.isdir(EXAMPLES_DIR):
        return rows

    for path in glob.glob(EXAMPLES_DIR + "/**/*", recursive=True):
        if not os.path.isfile(path):
            continue
        
        if not is_valid_code_file(path):
            continue
            
        fname = os.path.basename(path).lower()
        try:
            with open(path, "r", errors="ignore") as f:
                text = f.read()
        except Exception:
            continue

        if not text.strip():
            continue

        if fname.startswith("safe_"):
            label = "safe"
        elif "sqli" in fname or "sql" in fname:
            label = "sqli"
        elif "xss" in fname:
            label = "xss"
        elif "rce" in fname:
            label = "rce"
        elif "path_traversal" in fname or "path-traversal" in fname:
            label = "path_traversal"
        elif "deserialization" in fname:
            label = "deserialization"
        elif "weak_crypto" in fname or "weak-crypto" in fname:
            label = "weak_crypto"
        elif "vulnerable" in fname or "vulerable" in fname:
            label = "other_vuln"
        else:
            label = weak_label(text)

        rows.append({
            "source": "examples",
            "file_path": os.path.relpath(path, ROOT_DIR),
            "cve": None,
            "code": text,
            "label": label,
        })

    return rows

print("[+] Construyendo dataset a partir de PoCs, exploits, código seguro y REPOS REALES...")
print("[+] FILTRADO ACTIVO: Solo archivos de código, sin binarios")

all_rows: list[dict] = []

# 1) Vulnerabilidades reales (PoCs y exploits)
print("[+] Leyendo PoCs de GitHub...")
all_rows += read_text_files(GITHUB_POC_DIR, "github_poc", mode="vuln")

print("[+] Leyendo exploits de Searchsploit...")
all_rows += read_text_files(SEARCHSPLOIT_DIR, "searchsploit", mode="vuln")

# 2) NUEVO: Repositorios reales de vulnerabilidades
print("[+] Leyendo repositorios REALES de vulnerabilidades...")
all_rows += read_text_files(REAL_VULNS_DIR, "real_repos", mode="real_vuln")

# 3) Código seguro
print("[+] Leyendo código 'seguro' (dataset/safe_code)...")
all_rows += read_text_files(SAFE_CODE_DIR, "safe_code", mode="safe")

# 4) Ejemplos manuales
print("[+] Integrando ejemplos manuales (examples/)...")
all_rows += read_examples()

if not all_rows:
    print("[!] No se encontraron archivos de texto en ninguna fuente.")
    exit(1)

samples_df = pd.DataFrame(all_rows)
samples_df.insert(0, "id", range(1, len(samples_df) + 1))

# VALIDACIÓN
print(f"\n[+] Total de muestras antes de validación: {len(samples_df)}")
print("[+] Distribución de clases:")
class_counts = samples_df["label"].value_counts()
print(class_counts)

# Advertir sobre clases con pocas muestras
print("\n[!] VALIDACIÓN DE CLASES:")
for label, count in class_counts.items():
    if count < 5:
        print(f"  ⚠️  Clase '{label}' tiene solo {count} muestras (mínimo recomendado: 10)")
    elif count < 15:
        print(f"  ⚡ Clase '{label}' tiene {count} muestras (podría mejorar con más datos)")
    else:
        print(f"  ✅ Clase '{label}' tiene {count} muestras")

samples_csv_path = os.path.join(DATASET_DIR, "samples.csv")
samples_df.to_csv(samples_csv_path, index=False, escapechar='\\')
print(f"\n[+] samples.csv generado en: {samples_csv_path}")
print(f"[+] Distribución de fuentes:")
print(samples_df["source"].value_counts())

# === Generar TF-IDF ===
print("\n[+] Generando features TF-IDF...")

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2,
)

X = vectorizer.fit_transform(samples_df["code"].astype(str)).toarray()
features_df = pd.DataFrame(X)
features_df["label"] = samples_df["label"].values

features_csv = os.path.join(FEATURES_DIR, "features_tfidf.csv")
features_df.to_csv(features_csv, index=False)
print(f"[+] Features TF-IDF guardadas en: {features_csv}")

vec_path = os.path.join(MODELS_DIR, "vectorizer.pkl")
joblib.dump(vectorizer, vec_path)
print(f"[+] Vectorizer guardado en: {vec_path}")

print("\n[+] Construcción de dataset completa.")
print("[+] Siguiente paso: python3 6_train_model.py")
