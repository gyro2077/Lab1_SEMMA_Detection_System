#!/usr/bin/env python3
"""
Usa el modelo entrenado para predecir la clase de un archivo de código.
Ejemplo de uso:
    python3 predict_file.py ruta/al/archivo.c
"""

import os
import sys
import joblib

if len(sys.argv) < 2:
    print(f"Uso: {sys.argv[0]} /ruta/al/archivo")
    sys.exit(1)

file_path = sys.argv[1]

if not os.path.isfile(file_path):
    print(f"[!] No se encontró el archivo: {file_path}")
    sys.exit(1)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(ROOT_DIR, "models", "model_pipeline.pkl")

if not os.path.exists(MODEL_PATH):
    print(f"[!] No se encontró el modelo en {MODEL_PATH}. "
          f"Ejecuta primero train_model.py")
    sys.exit(1)

print(f"[+] Cargando modelo desde: {MODEL_PATH}")
pipeline = joblib.load(MODEL_PATH)

with open(file_path, "r", errors="ignore") as f:
    code = f.read()

pred = pipeline.predict([code])[0]
proba = pipeline.predict_proba([code])[0]
classes = pipeline.classes_

# probabilidad de la clase predicha
pred_idx = list(classes).index(pred)
confidence = proba[pred_idx]

print(f"[+] Archivo: {file_path}")
print(f"[+] Clase predicha: {pred}")
print(f"[+] Confianza   : {confidence:.2f}")
