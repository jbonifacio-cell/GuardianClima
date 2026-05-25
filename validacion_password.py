"""
validacion_password.py - Validación de Contraseñas
Implementa lógica de validación y feedback para contraseñas seguras.

Desarrollado por: Grupo 56 - ITBA 2026
"""

import re


def validar_password(password):
    """
    Valida que la contraseña cumpla con todos los requisitos de seguridad.
    
    Requisitos:
    - Mínimo 8 caracteres
    - Al menos una MAYÚSCULA
    - Al menos una minúscula
    - Al menos un número
    - Al menos un carácter especial (!@#$%^&*...)
    
    Retorna:
    - (True, []) si la contraseña es válida
    - (False, [lista de reglas incumplidas]) si no es válida
    """
    reglas_incumplidas = []
    
    # 1. Validar longitud mínima
    if len(password) < 8:
        reglas_incumplidas.append("Mínimo 8 caracteres")
    
    # 2. Validar que tenga al menos una MAYÚSCULA
    if not re.search(r'[A-Z]', password):
        reglas_incumplidas.append("Al menos una MAYÚSCULA")
    
    # 3. Validar que tenga al menos una minúscula
    if not re.search(r'[a-z]', password):
        reglas_incumplidas.append("Al menos una minúscula")
    
    # 4. Validar que tenga al menos un número
    if not re.search(r'\d', password):
        reglas_incumplidas.append("Al menos un número")
    
    # 5. Validar que tenga al menos un carácter especial
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        reglas_incumplidas.append("Al menos un carácter especial (!@#$%...)")
    
    # Si no hay reglas incumplidas, la contraseña es válida
    es_valida = len(reglas_incumplidas) == 0
    
    return es_valida, reglas_incumplidas


def mostrar_feedback_password(reglas_incumplidas):
    """
    Muestra feedback visual sobre qué requisitos no cumple la contraseña.
    Proporciona sugerencias de mejora.
    
    Parámetro:
    - reglas_incumplidas: lista de requisitos no cumplidos
    """
    print("\n ❌ La contraseña no cumple con los requisitos:")
    for regla in reglas_incumplidas:
        print(f"    • {regla}")
    
    print("\n 💡 Ejemplo de contraseña robusta: Admin@2024")


def sugerir_password_robusta():
    """
    Genera y sugiere una contraseña robusta como ejemplo.
    
    Retorna:
    - Una sugerencia de contraseña que cumple todos los requisitos
    """
    sugerencia = "Admin@2024"
    return sugerencia
