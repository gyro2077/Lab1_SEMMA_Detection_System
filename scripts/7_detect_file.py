#!/usr/bin/env python3
"""
Detección de vulnerabilidades en un archivo de código usando:
 - models/vectorizer.pkl
 - models/model_rf.pkl

Muestra:
 - Clase predicha
 - Confianza
 - Probabilidades por clase (con barras)
 - CVE IDs encontrados en el archivo (si existen)
"""

import os
import sys
import re
import joblib
import numpy as np

# Colores ANSI para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Emojis y descripciones por tipo de vulnerabilidad
VULN_INFO = {
    "sqli": {
        "emoji": "💉",
        "name": "SQL Injection",
        "description": "Inyección de comandos SQL en consultas de base de datos",
        "severity": "CRÍTICA"
    },
    "xss": {
        "emoji": "🌐",
        "name": "Cross-Site Scripting",
        "description": "Ejecución de scripts maliciosos en navegadores de usuarios",
        "severity": "ALTA"
    },
    "rce": {
        "emoji": "💣",
        "name": "Remote Code Execution",
        "description": "Ejecución remota de código arbitrario en el sistema",
        "severity": "CRÍTICA"
    },
    "path_traversal": {
        "emoji": "📂",
        "name": "Path Traversal",
        "description": "Acceso no autorizado a archivos del sistema",
        "severity": "ALTA"
    },
    "deserialization": {
        "emoji": "📦",
        "name": "Unsafe Deserialization",
        "description": "Deserialización insegura de objetos",
        "severity": "CRÍTICA"
    },
    "weak_crypto": {
        "emoji": "🔓",
        "name": "Weak Cryptography",
        "description": "Uso de algoritmos criptográficos débiles",
        "severity": "MEDIA"
    },
    "other_vuln": {
        "emoji": "⚠️",
        "name": "Otra Vulnerabilidad",
        "description": "Vulnerabilidad no clasificada en categorías específicas",
        "severity": "VARIABLE"
    },
    "safe": {
        "emoji": "✅",
        "name": "Código Seguro",
        "description": "No se detectaron patrones de vulnerabilidades conocidas",
        "severity": "NINGUNA"
    }
}


def find_cves(text: str) -> list[str]:
    """Devuelve una lista de CVE IDs encontrados en el texto."""
    return sorted(set(re.findall(r"CVE-\d{4}-\d+", text, flags=re.IGNORECASE)))


def print_header():
    """Imprime el header del análisis."""
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKCYAN}  🔍 DETECTOR DE VULNERABILIDADES - SEMMA ML Security Scanner{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKCYAN}{'='*70}{Colors.ENDC}\n")


def print_file_info(file_path, file_size):
    """Imprime información del archivo analizado."""
    print(f"{Colors.BOLD}📄 Archivo:{Colors.ENDC} {file_path}")
    print(f"{Colors.BOLD}📊 Tamaño:{Colors.ENDC} {file_size:,} bytes")


def print_vulnerability_detail(pred):
    """Imprime detalles de la vulnerabilidad detectada."""
    info = VULN_INFO.get(pred, VULN_INFO["other_vuln"])
    
    print(f"\n{Colors.BOLD}🎯 CATEGORÍA DETECTADA:{Colors.ENDC}")
    print(f"   {info['emoji']} {Colors.BOLD}{info['name']}{Colors.ENDC}")
    print(f"   {Colors.BOLD}Descripción:{Colors.ENDC} {info['description']}")
    print(f"   {Colors.BOLD}Severidad:{Colors.ENDC} {info['severity']}")


def print_prob_bars(classes, probs):
    """Imprime las probabilidades por clase con barras de colores."""
    print(f"\n{Colors.BOLD}📈 DISTRIBUCIÓN DE PROBABILIDADES:{Colors.ENDC}\n")
    
    # Ordenar por probabilidad
    sorted_data = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)
    
    for cls, p in sorted_data:
        # Color según probabilidad
        if p >= 0.7:
            color = Colors.FAIL
        elif p >= 0.5:
            color = Colors.WARNING
        elif p >= 0.3:
            color = Colors.OKCYAN
        else:
            color = Colors.ENDC
        
        # Barra visual
        bar_length = int(p * 40)
        bar = "█" * bar_length
        empty_bar = "░" * (40 - bar_length)
        
        # Emoji de la categoría
        emoji = VULN_INFO.get(cls, {}).get("emoji", "❓")
        
        print(f"   {emoji} {cls:<20s} {color}{p*100:6.2f}%{Colors.ENDC} {color}{bar}{Colors.ENDC}{empty_bar}")


def print_cve_ids(cve_ids):
    """Imprime CVEs encontrados en el archivo."""
    if cve_ids:
        print(f"\n{Colors.BOLD}🔖 CVE IDs DETECTADOS EN EL CÓDIGO:{Colors.ENDC}")
        for c in cve_ids:
            print(f"   • {Colors.WARNING}{c}{Colors.ENDC}")
    else:
        print(f"\n{Colors.BOLD}ℹ️  No se detectaron CVE IDs explícitos en el archivo.{Colors.ENDC}")


def print_threat_assessment(pred, confidence):
    """Imprime la evaluación de amenaza."""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
    
    if pred != "safe":
        if confidence >= 0.70:
            print(f"{Colors.FAIL}{Colors.BOLD}")
            print("⚠️  ⚠️  ⚠️  ALERTA CRÍTICA  ⚠️  ⚠️  ⚠️")
            print(f"{Colors.ENDC}")
            print(f"{Colors.FAIL}Posible vulnerabilidad {VULN_INFO[pred]['name']} detectada{Colors.ENDC}")
            print(f"{Colors.BOLD}Confianza:{Colors.ENDC} {Colors.FAIL}{confidence*100:.2f}%{Colors.ENDC}")
            print(f"\n{Colors.BOLD}🚨 ACCIÓN REQUERIDA:{Colors.ENDC}")
            print("   1. Realizar análisis manual profundo inmediatamente")
            print("   2. No desplegar este código en producción")
            print("   3. Contactar al equipo de seguridad")
            print("   4. Documentar el hallazgo en el sistema de tracking")
        elif confidence >= 0.50:
            print(f"{Colors.WARNING}{Colors.BOLD}")
            print("⚡ ADVERTENCIA - Posible Vulnerabilidad")
            print(f"{Colors.ENDC}")
            print(f"{Colors.WARNING}Tipo: {VULN_INFO[pred]['name']}{Colors.ENDC}")
            print(f"{Colors.BOLD}Confianza:{Colors.ENDC} {Colors.WARNING}{confidence*100:.2f}%{Colors.ENDC}")
            print(f"\n{Colors.BOLD}📋 ACCIÓN RECOMENDADA:{Colors.ENDC}")
            print("   • Revisión manual recomendada")
            print("   • Verificar contexto del código")
            print("   • Considerar análisis adicional")
        else:
            print(f"{Colors.OKCYAN}{Colors.BOLD}")
            print("ℹ️  Nivel de confianza bajo")
            print(f"{Colors.ENDC}")
            print(f"Predicción: {VULN_INFO[pred]['name']}")
            print(f"{Colors.BOLD}Confianza:{Colors.ENDC} {confidence*100:.2f}%")
            print(f"\n{Colors.BOLD}💡 SUGERENCIA:{Colors.ENDC}")
            print("   • Puede revisarse opcionalmente")
            print("   • No se considera crítico")
    else:
        print(f"{Colors.OKGREEN}{Colors.BOLD}")
        print("✅ ✅ ✅  CÓDIGO SEGURO  ✅ ✅ ✅")
        print(f"{Colors.ENDC}")
        print(f"{Colors.OKGREEN}No se detectaron vulnerabilidades con alta confianza{Colors.ENDC}")
        print(f"{Colors.BOLD}Confianza:{Colors.ENDC} {Colors.OKGREEN}{confidence*100:.2f}%{Colors.ENDC}")
        print(f"\n{Colors.BOLD}✨ El código parece seguir buenas prácticas de seguridad{Colors.ENDC}")
    
    print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{Colors.FAIL}Uso: {sys.argv[0]} /ruta/al/archivo{Colors.ENDC}")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"{Colors.FAIL}[!] Archivo no encontrado: {file_path}{Colors.ENDC}")
        sys.exit(1)

    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    MODELS_DIR = os.path.join(ROOT_DIR, "models")

    vec_path = os.path.join(MODELS_DIR, "vectorizer.pkl")
    model_path = os.path.join(MODELS_DIR, "model_rf.pkl")

    if not os.path.exists(vec_path) or not os.path.exists(model_path):
        print(f"{Colors.FAIL}[!] No se encontró vectorizer o modelo.{Colors.ENDC}")
        print("    Ejecuta primero 5_make_features.py y 6_train_model.py.")
        sys.exit(1)

    # Header
    print_header()

    # Info del archivo
    file_size = os.path.getsize(file_path)
    print_file_info(file_path, file_size)

    # Cargar modelo
    print(f"\n{Colors.OKCYAN}[+] Cargando modelo de ML...{Colors.ENDC}")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)

    # Leer y analizar archivo
    with open(file_path, "r", errors="ignore") as f:
        code = f.read()

    print(f"{Colors.OKCYAN}[+] Analizando código...{Colors.ENDC}")
    
    X_vec = vectorizer.transform([code])
    X = X_vec.toarray()

    classes = model.classes_
    probs = model.predict_proba(X)[0]
    pred = classes[np.argmax(probs)]
    confidence = np.max(probs)

    # Buscar CVEs en el código
    cve_ids = find_cves(code)

    # Resultados
    print_vulnerability_detail(pred)
    print_prob_bars(classes, probs)
    print_cve_ids(cve_ids)
    print_threat_assessment(pred, confidence)
