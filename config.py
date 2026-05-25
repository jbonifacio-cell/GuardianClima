"""
config.py - Configuración de la Aplicación
Almacena rutas de archivos y variables globales de configuración.
Las API Keys se cargan desde variables de entorno por seguridad.

Desarrollado por: Grupo 56 - ITBA 2026
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# ========== CONFIGURACIÓN DE API KEYS ==========
# ⚠️ IMPORTANTE: Las API Keys NO deben estar en el código fuente.
# Se cargan desde variables de entorno definidas en archivo .env (no commiteado)
# Si alguna API Key es None, la aplicación funcionará pero sin esa funcionalidad.

OWM_API_KEY = os.getenv("OWM_API_KEY", None)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", None)

# ========== CONFIGURACIÓN DE ARCHIVOS CSV ==========
# Rutas donde se almacenan datos de usuarios e historial global
ARCHIVO_USUARIOS = "usuarios_simulados.csv"
ARCHIVO_HISTORIAL = "historial_global.csv"

# ========== VALIDACIÓN DE CONFIGURACIÓN ==========
# Mostrar advertencia si las API Keys no están configuradas
if not OWM_API_KEY:
    print("⚠️  ADVERTENCIA: OWM_API_KEY no configurada. Revisa tu archivo .env")

if not GEMINI_API_KEY:
    print("⚠️  ADVERTENCIA: GEMINI_API_KEY no configurada. Revisa tu archivo .env")
