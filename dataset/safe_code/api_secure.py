#!/usr/bin/env python3
"""
Ejemplo de código seguro - API REST con validación
"""

from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Lista blanca de caracteres permitidos
ALLOWED_CHARS = re.compile(r'^[a-zA-Z0-9_-]+$')

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Obtiene información de usuario de forma segura."""
    
    # Validación de entrada
    if not ALLOWED_CHARS.match(user_id):
        return jsonify({'error': 'Invalid user ID format'}), 400
    
    # Usar consultas parametrizadas (no mostrado aquí)
    # db.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    
    return jsonify({'user_id': user_id, 'status': 'active'})

@app.route('/api/search', methods=['POST'])
def search():
    """Búsqueda segura con sanitización de entrada."""
    
    data = request.get_json()
    query = data.get('query', '')
    
    # Limitar longitud
    if len(query) > 100:
        return jsonify({'error': 'Query too long'}), 400
    
    # Escapar caracteres especiales
    safe_query = query.replace('<', '').replace('>', '').replace('"', '')
    
    # Búsqueda segura (ejemplo simplificado)
    results = []
    
    return jsonify({'query': safe_query, 'results': results})

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1')
