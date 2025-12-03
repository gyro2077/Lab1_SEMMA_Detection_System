#!/usr/bin/env python3
# Ejemplo de código seguro

def calculate_sum(numbers):
    """Calcula la suma de una lista de números."""
    return sum(numbers)

def greet_user(name):
    """Saluda al usuario de forma segura."""
    # Sanitiza el input
    safe_name = str(name).replace('<', '').replace('>', '')
    return f"Hola, {safe_name}!"

class Calculator:
    """Calculadora simple y segura."""
    
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("No se puede dividir por cero")
        return a / b

if __name__ == "__main__":
    calc = Calculator()
    result = calc.add(5, 3)
    print(f"Resultado: {result}")
