#!/usr/bin/env python3
"""
Construcción de dataset samples.csv + features TF-IDF a partir de:
 - PoCs de GitHub          (dataset/github_poc)
 - Exploits de Searchsploit (dataset/searchsploit)
 - Código "seguro"         (dataset/safe_code)
 - Ejemplos manuales       (examples/)

Salida:
 - dataset/samples.csv               (id, source, file_path, cve, code, label)
 - dataset/features/features_tfidf.csv
 - models/vectorizer.pkl
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

FEATURES_DIR = os.path.join(DATASET_DIR, "features")
MODELS_DIR = os.path.join(ROOT_DIR, "models")

os.makedirs(FEATURES_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Mapeo manual CVE -> tipo principal de vulnerabilidad
CVE_TYPE_MAP = {
    "CVE-2020-1472": "rce",           # Zerologon
    "CVE-2021-3156": "rce",           # sudo heap overflow / priv esc
    "CVE-2021-44228": "rce",          # Log4Shell
    "CVE-2023-38831": "rce",          # WinRAR RCE
    "CVE-2023-36884": "rce",          # Office RCE
    "CVE-2019-0708": "rce",           # BlueKeep
    # Aquí puedes añadir más CVE -> tipo según lo que estudies
}


def extract_cve_from_path(path: str) -> str | None:
    """
    Intenta extraer un CVE desde la ruta del archivo.
    Ej: .../CVE-2021-44228/poc.py -> CVE-2021-44228
    """
    m = re.search(r"CVE-\d{4}-\d+", path, re.IGNORECASE)
    if m:
        return m.group(0).upper()
    return None


def weak_label(text: str) -> str:
    """
    Asigna etiquetas débiles según patrones típicos.
    Esto es heurístico, sirve para construir un dataset grande.
    """
    t = text.lower()

    # SQL Injection
    if re.search(r"(select\s+.+\s+from|union\s+select|or\s+1=1|information_schema)", t):
        return "sqli"

    # XSS
    if re.search(r"(<script|onerror=|onload=|document\.cookie|innerhtml)", t):
        return "xss"

    # RCE / Command injection
    if re.search(
        r"(system\(|exec\(|popen\(|runtime\.getruntime\(\)|processbuilder|shell_exec|`.+`)",
        t,
    ):
        return "rce"

    # Path traversal
    if re.search(r"(\.\./|\.\.\\|/etc/passwd|c:\\\\windows\\\\)", t):
        return "path_traversal"

    # Deserialización insegura
    if re.search(r"(objectinputstream|readobject\(|pickle\.loads|yaml\.load\()", t):
        return "deserialization"

    # Cripto débil
    if re.search(r"(md5\(|sha1\(|des_crypt|rc4|cipher\.getinstance\(\"des)", t):
        return "weak_crypto"

    return "other_vuln"


def read_text_files(base_dir: str, source: str, mode: str) -> list[dict]:
    """
    Lee archivos de texto desde base_dir.
    mode:
      - "vuln": etiqueta con weak_label + CVE_TYPE_MAP
      - "safe": etiqueta como 'safe'
    """
    rows: list[dict] = []
    if not os.path.isdir(base_dir):
        print(f"[!] Directorio no encontrado, se omite: {base_dir}")
        return rows

    for path in glob.glob(base_dir + "/**/*", recursive=True):
        if not os.path.isfile(path):
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
        else:
            label = weak_label(text)
            # Si tenemos CVE -> sobreescribimos por tipo conocido
            if cve and cve in CVE_TYPE_MAP:
                label = CVE_TYPE_MAP[cve]

        rows.append(
            {
                "source": source,
                "file_path": rel_path,
                "cve": cve,
                "code": text,
                "label": label,
            }
        )
    return rows


def read_examples() -> list[dict]:
    """
    Integra explícitamente los ejemplos de ../examples:
      - vulnerable_sqli.php  -> sqli
      - vulnerable_xss.js    -> xss
      - vulnerable_rce.py    -> rce
      - safe_code.py         -> safe
      - cualquier otro 'vulnerable_*.ext' -> other_vuln
    """
    rows: list[dict] = []
    if not os.path.isdir(EXAMPLES_DIR):
        return rows

    for path in glob.glob(EXAMPLES_DIR + "/**/*", recursive=True):
        if not os.path.isfile(path):
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
        elif "sqli" in fname:
            label = "sqli"
        elif "xss" in fname:
            label = "xss"
        elif "rce" in fname:
            label = "rce"
        elif "vulnerable" in fname or "vulerable" in fname:
            label = "other_vuln"
        else:
            # Si no matchea nada específico, usamos heurística
            label = weak_label(text)

        rows.append(
            {
                "source": "examples",
                "file_path": os.path.relpath(path, ROOT_DIR),
                "cve": None,
                "code": text,
                "label": label,
            }
        )

    return rows


print("[+] Construyendo dataset a partir de PoCs, exploits y código seguro...")

all_rows: list[dict] = []

# 1) Vulnerabilidades reales (PoCs y exploits)
print("[+] Leyendo PoCs de GitHub...")
all_rows += read_text_files(GITHUB_POC_DIR, "github_poc", mode="vuln")

print("[+] Leyendo exploits de Searchsploit...")
all_rows += read_text_files(SEARCHSPLOIT_DIR, "searchsploit", mode="vuln")

# 2) Código seguro
print("[+] Leyendo código 'seguro' (dataset/safe_code)...")
all_rows += read_text_files(SAFE_CODE_DIR, "safe_code", mode="safe")

# 3) Ejemplos manuales
print("[+] Integrando ejemplos manuales (examples/)...")
all_rows += read_examples()

if not all_rows:
    print("[!] No se encontraron archivos de texto en ninguna fuente.")
    print("    Ejecuta 1_github_poc.sh, 2_searchsploit.sh y/o llena dataset/safe_code y examples/")
    exit(1)

samples_df = pd.DataFrame(all_rows)
samples_df.insert(0, "id", range(1, len(samples_df) + 1))

samples_csv_path = os.path.join(DATASET_DIR, "samples.csv")
samples_df.to_csv(samples_csv_path, index=False)
print(f"[+] samples.csv generado en: {samples_csv_path}")
print(f"[+] Total de muestras: {len(samples_df)}")
print("[+] Distribución de clases:")
print(samples_df["label"].value_counts())
print("[+] Distribución de fuentes:")
print(samples_df["source"].value_counts())

# === Generar TF-IDF ===
print("[+] Generando features TF-IDF...")

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

print("[+] Construcción de dataset completa.")
print("[+] Siguiente paso: python3 6_train_model.py")
