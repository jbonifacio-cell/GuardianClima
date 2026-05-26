"""
clima.py - Módulo de Consulta de Clima, conectado a la API de OpenWeatherMap para obtener datos climáticos en tiempo real.

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
    Retorna un dict con los datos del clima, o None si hay error.
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
        if respuesta.status_code == 401:
            print(" Error de autenticación: API Key de OWM inválida.")
            print("   Revisá tu API Key en config.py")
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
    Extrae y estructura los datos relevantes del JSON de OWM.
    
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
    """Muestra el clima de forma clara y ordenada."""

    print(f"  Clima en {datos['ciudad']}, {datos['pais']}")
    print(f"  Temperatura:       {datos['temperatura']}°C")
    print(f"  Sensación térmica: {datos['sensacion_termica']}°C")
    print(f"  Humedad:           {datos['humedad']}%")
    print(f"  Viento:            {datos['viento_kmh']} km/h")
    print(f"  Condición:         {datos['descripcion']}")
    


def inicializar_historial():
    """Crea el archivo CSV de historial si no existe."""
    if not os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "NombreDeUsuario", "Ciudad", "FechaHora",
                "Temperatura_C", "Condicion_Clima",
                "Humedad_Porcentaje", "Viento_kmh"
            ])


def guardar_en_historial(username, datos):
    """Guarda una consulta de clima en el historial global CSV."""
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
    Opción 1 del menú principal, consulta el clima de una ciudad y lo guarda en el historial.
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
    Opción 2 del menú principal, muestra el historial de consultas del usuario para una ciudad específica.
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
