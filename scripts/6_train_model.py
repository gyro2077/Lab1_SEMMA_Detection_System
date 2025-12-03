#!/usr/bin/env python3
"""
Entrenamiento de RandomForest sobre features TF-IDF.
Lee:
  - dataset/features/features_tfidf.csv
  - models/vectorizer.pkl (para mostrar features importantes)

Guarda:
  - models/model_rf.pkl
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FEATURES_DIR = os.path.join(ROOT_DIR, "dataset", "features")
MODELS_DIR = os.path.join(ROOT_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

features_csv = os.path.join(FEATURES_DIR, "features_tfidf.csv")
if not os.path.exists(features_csv):
    print("[!] No se encontró features_tfidf.csv. Ejecuta primero 5_make_features.py")
    exit(1)

print(f"[+] Cargando features desde: {features_csv}")
df = pd.read_csv(features_csv)

if "label" not in df.columns:
    raise ValueError("El CSV de features debe contener la columna 'label'")

X = df.drop("label", axis=1).values  # <-- sin nombres de columnas
y = df["label"].astype(str).values

print(f"[+] Total de muestras: {len(y)}")
print(f"[+] Total de features: {X.shape[1]}")
print("[+] Distribución de clases:")
print(pd.Series(y).value_counts())

# Check if we can stratify (need at least 2 samples per class)
class_counts = pd.Series(y).value_counts()
can_stratify = all(count >= 2 for count in class_counts)

if not can_stratify:
    print("[!] Algunas clases tienen solo 1 muestra. Entrenando sin estratificación...")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )
else:
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

print(f"[+] Tamaño train: {X_train.shape[0]}")
print(f"[+] Tamaño test : {X_test.shape[0]}")
print(f"[+] Clases: {sorted(set(y))}")

clf = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    n_jobs=-1,
    random_state=42,
    class_weight="balanced",
)

print("[+] Entrenando RandomForest...")
clf.fit(X_train, y_train)

print("[+] Evaluación en conjunto de prueba:")
y_pred = clf.predict(X_test)
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, digits=4, zero_division=0))

print("\n=== Matriz de confusión ===")
print(confusion_matrix(y_test, y_pred))

# Guardar modelo
model_path = os.path.join(MODELS_DIR, "model_rf.pkl")
joblib.dump(clf, model_path)
print(f"\n[+] Modelo guardado en: {model_path}")

# Mostrar features importantes (top 20)
vec_path = os.path.join(MODELS_DIR, "vectorizer.pkl")
if os.path.exists(vec_path):
    print("\n[+] Calculando importancia de features (top 20)...")
    vectorizer = joblib.load(vec_path)
    feature_names = vectorizer.get_feature_names_out()
    importances = clf.feature_importances_

    # Ordenar por importancia
    idxs = importances.argsort()[::-1][:20]
    print("\n=== Top 20 features importantes ===")
    for i in idxs:
        print(f"{feature_names[i]:30s}  {importances[i]:.5f}")
else:
    print("[!] No se encontró vectorizer.pkl, no se pueden mostrar features importantes.")

print("\n[+] Entrenamiento completo.")
print("[+] Para usar el modelo: python3 7_detect_file.py <archivo>")
