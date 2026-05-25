"""
clima.py - Módulo de Consulta de Clima
Conectado a la API de OpenWeatherMap para obtener datos climáticos en tiempo real.
Maneja consultas, almacenamiento en historial y visualización de datos.

Desarrollado por: Grupo 56 - ITBA 2026
"""

import requests
import json
import csv
import os
from datetime import datetime
from config import OWM_API_KEY, ARCHIVO_HISTORIAL


def obtener_clima_ciudad_owm(ciudad):
    """
    Consulta el clima actual de una ciudad usando OpenWeatherMap.
    
    Parámetro:
    - ciudad: nombre de la ciudad a consultar
    
    Retorna:
    - dict con los datos del clima si es exitoso
    - None si hay error (API no disponible, ciudad no encontrada, etc.)
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    parametros = {
        'q': ciudad,
        'appid': OWM_API_KEY,
        'units': 'metric',
        'lang': 'es'
    }

    print(f"\n Consultando el clima para: {ciudad}...")

    try:
        respuesta = requests.get(base_url, params=parametros, timeout=10)
        respuesta.raise_for_status()
        datos_clima = respuesta.json()
        return datos_clima

    except requests.exceptions.HTTPError as errh:
        # Manejo específico de errores HTTP
        if respuesta.status_code == 401:
            print(" Error de autenticación: API Key de OWM inválida.")
            print("   Revisá tu API Key en archivo .env")
        elif respuesta.status_code == 404:
            print(f" Ciudad '{ciudad}' no encontrada. Verificá el nombre e intentá de nuevo.")
        else:
            print(f" Error HTTP: {errh}")
        return None

    except requests.exceptions.ConnectionError:
        print(" Error de conexión. Verificá tu acceso a internet.")
        return None

    except requests.exceptions.Timeout:
        print(" La solicitud tardó demasiado. Intentá de nuevo.")
        return None

    except requests.exceptions.RequestException as err:
        print(f" Error en la petición: {err}")
        return None

    except json.JSONDecodeError:
        print(" Error: La respuesta de la API no es válida.")
        return None


def parsear_datos_clima(datos_raw):
    """
    Extrae y estructura los datos relevantes del JSON de OpenWeatherMap.
    
    Parámetro:
    - datos_raw: respuesta JSON cruda de la API
    
    Retorna:
    - dict con campos formateados (ciudad, pais, temperatura, etc.)
    - None si hay error en la extracción de datos
    """
    try:
        ciudad = datos_raw.get('name', 'Desconocida')
        pais = datos_raw.get('sys', {}).get('country', '??')
        temperatura = round(datos_raw['main']['temp'], 1)
        sensacion_termica = round(datos_raw['main']['feels_like'], 1)
        humedad = datos_raw['main']['humidity']
        descripcion = datos_raw['weather'][0]['description'].capitalize()
        viento_ms = datos_raw['wind']['speed']
        viento_kmh = round(viento_ms * 3.6, 1)

        return {
            'ciudad': ciudad,
            'pais': pais,
            'temperatura': temperatura,
            'sensacion_termica': sensacion_termica,
            'humedad': humedad,
            'descripcion': descripcion,
            'viento_kmh': viento_kmh,
        }
    except KeyError as e:
        print(f" Error al procesar datos del clima: campo faltante {e}")
        return None


def mostrar_clima(datos):
    """
    Muestra el clima de forma clara y ordenada en consola.
    
    Parámetro:
    - datos: dict con información del clima (resultado de parsear_datos_clima)
    """
    print(f"\n  Clima en {datos['ciudad']}, {datos['pais']}")
    print(f"  Temperatura:       {datos['temperatura']}°C")
    print(f"  Sensación térmica: {datos['sensacion_termica']}°C")
    print(f"  Humedad:           {datos['humedad']}%")
    print(f"  Viento:            {datos['viento_kmh']} km/h")
    print(f"  Condición:         {datos['descripcion']}")


def inicializar_historial():
    """
    Crea el archivo CSV de historial global si no existe.
    Define las columnas para almacenar historial de consultas.
    """
    if not os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "NombreDeUsuario", "Ciudad", "FechaHora",
                "Temperatura_C", "Condicion_Clima",
                "Humedad_Porcentaje", "Viento_kmh"
            ])


def guardar_en_historial(username, datos):
    """
    Guarda una consulta de clima en el historial global CSV.
    Permite análisis posterior y generación de estadísticas.
    
    Parámetros:
    - username: usuario que realizó la consulta
    - datos: dict con información del clima a guardar
    """
    inicializar_historial()
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARCHIVO_HISTORIAL, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            username,
            datos['ciudad'],
            fecha_hora,
            datos['temperatura'],
            datos['descripcion'],
            datos['humedad'],
            datos['viento_kmh']
        ])
    print(f"\n Consulta guardada en historial global.")


def consultar_clima_y_guardar(username):
    """
    OPCIÓN 1 DEL MENÚ PRINCIPAL
    Consulta el clima de una ciudad y lo guarda en el historial.
    
    Flujo:
    1. Solicita nombre de la ciudad
    2. Consulta OpenWeatherMap
    3. Procesa datos
    4. Muestra resultado
    5. Guarda en historial
    
    Parámetro:
    - username: usuario autenticado
    
    Retorna:
    - dict con datos del clima si es exitoso
    - None si hay error
    """

    print("CONSULTAR CLIMA ACTUAL")

    ciudad = input("\nIngresá el nombre de la ciudad: ").strip()
    if not ciudad:
        print(" Nombre de ciudad inválido.")
        return None

    datos_raw = obtener_clima_ciudad_owm(ciudad)
    if not datos_raw:
        return None

    datos = parsear_datos_clima(datos_raw)
    if not datos:
        return None

    mostrar_clima(datos)
    guardar_en_historial(username, datos)
    return datos


def ver_historial_personal(username):
    """
    OPCIÓN 2 DEL MENÚ PRINCIPAL
    Muestra el historial de consultas del usuario para una ciudad específica.
    
    Flujo:
    1. Solicita ciudad a buscar
    2. Filtra registros del usuario para esa ciudad
    3. Muestra resultados en tabla
    
    Parámetro:
    - username: usuario autenticado
    """

    print("MI HISTORIAL PERSONAL")

    ciudad_buscar = input("\nIngresá el nombre de la ciudad a buscar: ").strip()
    if not ciudad_buscar:
        print("Nombre de ciudad inválido.")
        return

    inicializar_historial()

    try:
        with open(ARCHIVO_HISTORIAL, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            registros = [
                fila for fila in reader
                if fila["NombreDeUsuario"].lower() == username.lower()
                and fila["Ciudad"].lower() == ciudad_buscar.lower()
            ]
    except FileNotFoundError:
        print("No hay historial registrado aún.")
        return

    if not registros:
        print(f"\n No se encontraron consultas para '{ciudad_buscar}' con tu usuario.")
        return

    print(f"\n Historial de {username} para {ciudad_buscar} ({len(registros)} consulta(s)):")
    print(f"{'Fecha/Hora':<22} {'Temp(°C)':<10} {'Humedad':<10} {'Condición'}")
    for r in registros:
        print(f"{r['FechaHora']:<22} {r['Temperatura_C']:<10} {r['Humedad_Porcentaje']+'%':<10} {r['Condicion_Clima']}")
