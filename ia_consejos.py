"""
ia_consejos.py - Consejos de Vestimenta con IA
Genera consejos de vestimenta personalizados usando la API de Google Gemini.
Utiliza datos climáticos actuales o históricos del usuario.

Desarrollado por: Grupo 56 - ITBA 2026
"""

import csv
import os
from config import GEMINI_API_KEY, ARCHIVO_HISTORIAL


def obtener_consejo_ia_gemini(temperatura, condicion_clima, viento_kmh, humedad):
    """
    Genera un consejo de vestimenta usando la API de Google Gemini.
    
    Parámetros:
    - temperatura: temperatura actual en °C
    - condicion_clima: descripción de la condición (ej: "Nublado")
    - viento_kmh: velocidad del viento en km/h
    - humedad: humedad relativa en porcentaje
    
    Retorna:
    - texto del consejo si es exitoso
    - None si hay error
    """
    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')

        # Diseñar un prompt específico para obtener consejos de vestimenta
        prompt = (
            f"Eres un asistente de moda y clima. Con base en las siguientes condiciones "
            f"climáticas actuales, dá un consejo breve, práctico y amigable sobre cómo "
            f"vestirse para salir. Sé específico con las prendas recomendadas.\n\n"
            f"Condiciones climáticas:\n"
            f"- Temperatura: {temperatura}°C\n"
            f"- Condición del cielo: {condicion_clima}\n"
            f"- Viento: {viento_kmh} km/h\n"
            f"- Humedad: {humedad}%\n\n"
            f"Dá el consejo en español, en no más de 5 oraciones. "
            f"Empezá con una frase que describa el clima de forma amigable."
        )

        print("\n Generando consejo de vestimenta con IA...")
        response = model.generate_content(prompt)

        if response.text:
            return response.text
        else:
            print("La IA no pudo generar un consejo.")
            if hasattr(response, 'prompt_feedback'):
                print(f"   Razón: {response.prompt_feedback}")
            return None

    except ImportError:
        print("La librería 'google-generativeai' no está instalada.")
        print("   Ejecutá: pip install google-generativeai")
        return None
    except Exception as e:
        print(f" Error al contactar Gemini: {e}")
        return None


def obtener_ultima_consulta_usuario(username):
    """
    Obtiene la última consulta de clima del usuario desde el historial.
    
    Parámetro:
    - username: nombre de usuario
    
    Retorna:
    - dict con datos de la última consulta
    - None si no hay registros
    """
    if not os.path.exists(ARCHIVO_HISTORIAL):
        return None

    try:
        with open(ARCHIVO_HISTORIAL, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            registros_usuario = [
                fila for fila in reader
                if fila["NombreDeUsuario"].lower() == username.lower()
            ]

        if registros_usuario:
            return registros_usuario[-1]  # Retorna el último registro
        return None

    except (FileNotFoundError, KeyError):
        return None


def consejo_vestimenta_ia(username, ultima_consulta_sesion=None):
    """
    OPCIÓN 4 DEL MENÚ PRINCIPAL
    Obtiene datos climáticos y genera un consejo de vestimenta con IA.
    
    Flujo:
    1. Intenta usar la última consulta de la sesión actual
    2. Si no existe, busca en el historial global del usuario
    3. Si no hay nada, realiza una consulta nueva
    4. Genera consejo con IA Gemini
    
    Parámetros:
    - username: usuario autenticado
    - ultima_consulta_sesion: datos de la última consulta en la sesión actual (opcional)
    """

    print("CONSEJO IA: ¿CÓMO ME VISTO HOY?")

    datos_clima = None

    # ===== OPCIÓN 1: Intentar usar la última consulta de la sesión actual =====
    if ultima_consulta_sesion:
        print(f"\n Usando datos de tu última consulta: {ultima_consulta_sesion['ciudad']}")
        print(f"   Temperatura: {ultima_consulta_sesion['temperatura']}°C | "
              f"Condición: {ultima_consulta_sesion['descripcion']}")
        usar_ultima = input("\n¿Usar estos datos? (s/n): ").strip().lower()
        if usar_ultima == 's':
            datos_clima = {
                'temperatura': ultima_consulta_sesion['temperatura'],
                'descripcion': ultima_consulta_sesion['descripcion'],
                'viento_kmh': ultima_consulta_sesion['viento_kmh'],
                'humedad': ultima_consulta_sesion['humedad'],
                'ciudad': ultima_consulta_sesion['ciudad'],
            }

    # ===== OPCIÓN 2: Si no, buscar en historial global =====
    if not datos_clima:
        registro = obtener_ultima_consulta_usuario(username)
        if registro:
            print(f"\n Última consulta registrada: {registro['Ciudad']} ({registro['FechaHora']})")
            print(f"   Temperatura: {registro['Temperatura_C']}°C | Condición: {registro['Condicion_Clima']}")
            usar_historial = input("\n¿Usar estos datos del historial? (s/n): ").strip().lower()
            if usar_historial == 's':
                datos_clima = {
                    'temperatura': float(registro['Temperatura_C']),
                    'descripcion': registro['Condicion_Clima'],
                    'viento_kmh': float(registro['Viento_kmh']),
                    'humedad': float(registro['Humedad_Porcentaje']),
                    'ciudad': registro['Ciudad'],
                }

    # ===== OPCIÓN 3: Si no hay datos, realizar nueva consulta =====
    if not datos_clima:
        print("\n Realizando nueva consulta de clima para obtener el consejo...")
        from clima import obtener_clima_ciudad_owm, parsear_datos_clima, mostrar_clima
        ciudad = input("Ingresá el nombre de la ciudad: ").strip()
        if not ciudad:
            print("Ciudad inválida.")
            return

        datos_raw = obtener_clima_ciudad_owm(ciudad)
        if not datos_raw:
            return

        datos_clima = parsear_datos_clima(datos_raw)
        if not datos_clima:
            return
        mostrar_clima(datos_clima)

    # ===== GENERAR CONSEJO CON IA =====
    consejo = obtener_consejo_ia_gemini(
        temperatura=datos_clima['temperatura'],
        condicion_clima=datos_clima['descripcion'],
        viento_kmh=datos_clima['viento_kmh'],
        humedad=datos_clima['humedad']
    )

    if consejo:
        print("\n" + "=" * 55)
        print(" CONSEJO DE VESTIMENTA (por IA Gemini):")
        print(f"\n{consejo}\n")
    else:
        print("\n No se pudo obtener el consejo de IA en este momento.")
        print("   Verificá tu API Key de Gemini en archivo .env")
