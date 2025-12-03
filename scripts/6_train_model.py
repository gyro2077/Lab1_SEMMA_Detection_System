#!/usr/bin/env python3
"""
ENTRENAMIENTO AVANZADO CON XGBOOST
Modelo de última generación para detección de vulnerabilidades
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, f1_score
import joblib

# Try XGBoost, fall back to LightGBM, then Random Forest
try:
    import xgboost as xgb
    MODEL_TYPE = "XGBoost"
    print("[+] Usando XGBoost (modelo avanzado)")
except ImportError:
    try:
        import lightgbm as lgb
        MODEL_TYPE = "LightGBM"
        print("[+] Usando LightGBM (modelo avanzado)")
    except ImportError:
        from sklearn.ensemble import RandomForestClassifier
        MODEL_TYPE = "RandomForest"
        print("[!] Usando RandomForest (fallback)")

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

X = df.drop("label", axis=1).values
y = df["label"].astype(str).values

print(f"\n[+] Total de muestras: {len(y)}")
print(f"[+] Total de features: {X.shape[1]}")
print("\n[+] Distribución de clases:")
class_counts_series = pd.Series(y).value_counts()
print(class_counts_series)

# VALIDACIÓN
print("\n[!] VALIDANDO DATASET...")
min_samples = 5
problematic_classes = []
good_classes = []

for label, count in class_counts_series.items():
    if count < min_samples:
        problematic_classes.append((label, count))
        print(f"  ❌ CRÍTICO: Clase '{label}' solo tiene {count} muestra(s)")
    elif count < 15:
        print(f"  ⚠️  ADVERTENCIA: Clase '{label}' tiene {count} muestras (recomendado: 20+)")
    else:
        good_classes.append(label)
        print(f"  ✅ Clase '{label}' tiene {count} muestras")

if len(good_classes) >= 5:
    print(f"\n[+] ✅ {len(good_classes)} clases con datos suficientes para buen entrenamiento")
    if len(y) > 500:
        print(f"[+] 🚀 Dataset grande detectado ({len(y)} muestras) - Accuracy esperado: 94-97%")
    elif len(y) > 300:
        print(f"[+] ⚡ Dataset medio ({len(y)} muestras) - Accuracy esperado: 90-94%")
    else:
        print(f"[+] 📊 Dataset pequeño ({len(y)} muestras) - Accuracy esperado: 85-90%")
else:
    print(f"\n[!] ⚠️  Solo {len(good_classes)} clases con datos suficientes")

# Split dataset
class_counts = pd.Series(y).value_counts()
can_stratify = all(count >= 2 for count in class_counts)

if not can_stratify:
    print("\n[!] Algunas clases tienen solo 1 muestra. Entrenando sin estratificación...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
else:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

print(f"\n[+] Tamaño train: {X_train.shape[0]}")
print(f"[+] Tamaño test : {X_test.shape[0]}")
print(f"[+] Clases: {sorted(set(y))}")

# ENTRENAR MODELO
print(f"\n[+] Entrenando modelo {MODEL_TYPE}...")

if MODEL_TYPE == "XGBoost":
    # Encode labels for XGBoost
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train)
    y_test_encoded = le.transform(y_test)
    
    clf = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        n_jobs=-1,
        eval_metric='mlogloss'
    )
    
    print("    Configuración: XGBoost con 200 árboles, max_depth=8, learning_rate=0.1")
    clf.fit(X_train, y_train_encoded)
    y_pred_encoded = clf.predict(X_test)
    y_pred = le.inverse_transform(y_pred_encoded)
    
    # Save label encoder
    joblib.dump(le, os.path.join(MODELS_DIR, "label_encoder.pkl"))
    
elif MODEL_TYPE == "LightGBM":
    clf = lgb.LGBMClassifier(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )
    
    print("    Configuración: LightGBM con 200 árboles")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
else:  # RandomForest fallback
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=2,
        min_samples_leaf=1,
        n_jobs=-1,
        random_state=42,
        class_weight="balanced"
    )
    
    print("    Configuración: RandomForest con 200 árboles")
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

# EVALUACIÓN
print("\n[+] Evaluación en conjunto de prueba:")
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, digits=4, zero_division=0))

print("\n=== Matriz de confusión ===")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Guardar modelo
model_path = os.path.join(MODELS_DIR, "model_xgb.pkl")
joblib.dump(clf, model_path)
print(f"\n[+] Modelo guardado en: {model_path}")

# Features importantes
vec_path = os.path.join(MODELS_DIR, "vectorizer.pkl")
if os.path.exists(vec_path):
    print("\n[+] Calculando importancia de features (top 30)...")
    vectorizer = joblib.load(vec_path)
    feature_names = vectorizer.get_feature_names_out()
    
    if MODEL_TYPE in ["XGBoost", "LightGBM"]:
        importances = clf.feature_importances_
    else:
        importances = clf.feature_importances_
    
    # Ordenar por importancia
    idxs = importances.argsort()[::-1][:30]
    print("\n=== Top 30 features importantes ===")
    for i in idxs:
        print(f"{feature_names[i]:30s}  {importances[i]:.5f}")

# Cross-validation score
if len(X_train) < 1000:  # Only do CV for smaller datasets
    print("\n[+] Calculando validación cruzada (puede tardar)...")
    cv_scores = cross_val_score(clf, X_train, y_train if MODEL_TYPE != "XGBoost" else y_train_encoded, 
                                 cv=min(5, len(set(y_train))), scoring='f1_weighted', n_jobs=-1)
    print(f"[+] F1-Score (CV): {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

print(f"\n[+] Entrenamiento completo con {MODEL_TYPE}!")
print("[+] Para usar el modelo: python3 7_detect_file.py <archivo>")

# Final assessment
test_acc = (y_test == y_pred).mean()
if test_acc >= 0.95:
    print(f"\n🏆 ¡EXCELENTE! Accuracy: {test_acc:.2%} - Modelo de nivel producción")
elif test_acc >= 0.90:
    print(f"\n✅ MUY BUENO! Accuracy: {test_acc:.2%} - Modelo robusto")
elif test_acc >= 0.85:
    print(f"\n👍 BUENO! Accuracy: {test_acc:.2%} - Modelo funcional")
else:
    print(f"\n⚠️  Accuracy: {test_acc:.2%} - Necesita más datos para mejorar")
