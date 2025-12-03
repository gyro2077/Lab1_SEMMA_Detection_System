#!/usr/bin/env python3
"""
Entrenamiento de modelo de clasificación de vulnerabilidades en código fuente
Usa:
 - TF-IDF para vectorizar el código (features textuales)
 - RandomForestClassifier como modelo principal
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# === Configuración de rutas ===
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASET_PATH = os.path.join(ROOT_DIR, "dataset", "samples.csv")
MODELS_DIR = os.path.join(ROOT_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(
        f"No se encuentra el dataset en {DATASET_PATH}. "
        f"Asegúrate de generar samples.csv con columnas: id, code, label."
    )

print(f"[+] Cargando dataset desde: {DATASET_PATH}")
df = pd.read_csv(DATASET_PATH)

# Validación básica de columnas
required_cols = {"code", "label"}
if not required_cols.issubset(df.columns):
    raise ValueError(f"El CSV debe contener las columnas: {required_cols}")

X_text = df["code"].astype(str)
y = df["label"].astype(str)

print("[+] Tamaño del dataset:", len(df))
print("[+] Clases disponibles:", y.unique())

# === División train/test ===
X_train, X_test, y_train, y_test = train_test_split(
    X_text,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y  # mantiene proporción de clases
)

print("[+] Tamaño train:", len(X_train))
print("[+] Tamaño test :", len(X_test))

# === Construcción del pipeline ===
# 1) TfidfVectorizer: convierte texto a vectores numéricos
# 2) RandomForestClassifier: modelo de clasificación
pipeline = make_pipeline(
    TfidfVectorizer(
        max_features=5000,        # número máximo de términos
        ngram_range=(1, 2),       # unigrams y bigrams
        min_df=2                  # ignora términos muy raros
    ),
    RandomForestClassifier(
        n_estimators=200,         # número de árboles
        n_jobs=-1,                # usa todos los núcleos disponibles
        random_state=42,
        class_weight="balanced"   # ayuda con datos desbalanceados
    )
)

print("[+] Entrenando modelo...")
pipeline.fit(X_train, y_train)

print("[+] Evaluando modelo...")
y_pred = pipeline.predict(X_test)

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, digits=4))

print("\n=== Matriz de confusión ===")
print(confusion_matrix(y_test, y_pred))

# === Guardar modelo entrenado ===
model_path = os.path.join(MODELS_DIR, "model_pipeline.pkl")
joblib.dump(pipeline, model_path)
print(f"\n[+] Modelo entrenado guardado en: {model_path}")
print("[+] Entrenamiento completo.")
