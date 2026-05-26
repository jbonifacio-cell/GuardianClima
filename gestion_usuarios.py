"""
estadisticas.py - Estadísticas Globales de Uso, procesa el historial global para generar estadísticas
y exportar datos para gráficos en Excel/Google Sheets.
"""

import csv
import os
from collections import Counter
from config import ARCHIVO_HISTORIAL


def calcular_estadisticas_globales():
    """
    Opción 3 del menú principal.
    Calcula y muestra estadísticas sobre todas las consultas de todos los usuarios.
    """

    print("ESTADÍSTICAS GLOBALES DE USO")

    if not os.path.exists(ARCHIVO_HISTORIAL):
        print("No hay datos en el historial global aún.")
        print(" Realizá algunas consultas de clima primero (Opción 1).")
        return

    try:
        with open(ARCHIVO_HISTORIAL, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            registros = list(reader)
    except FileNotFoundError:
        print("No se encontró el archivo de historial.")
        return

    if not registros:
        print("El historial está vacío. Realizá consultas primero.")
        return

    # 1: Total de consultas
    total_consultas = len(registros)

    # 2: Ciudad más consultada
    ciudades = [r["Ciudad"] for r in registros]
    conteo_ciudades = Counter(ciudades)
    ciudad_top = conteo_ciudades.most_common(1)[0]

    # 3: Temperatura promedio global
    temperaturas = []
    for r in registros:
        try:
            temperaturas.append(float(r["Temperatura_C"]))
        except (ValueError, KeyError):
            pass

    temp_promedio = round(sum(temperaturas) / len(temperaturas), 1) if temperaturas else 0

    # Mostrar resultados
    print(f"\n  Total de consultas realizadas:  {total_consultas}")
    print(f"  Ciudad más consultada:          {ciudad_top[0]} ({ciudad_top[1]} consultas)")
    print(f"  Temperatura promedio global:    {temp_promedio}°C")

    # Ranking de ciudades
    print(f"\n  Ranking de ciudades consultadas:")
    print("  " + "-" * 35)
    for i, (ciudad, count) in enumerate(conteo_ciudades.most_common(), 1):
        barra = "█" * count
        print(f"  {i:2}. {ciudad:<20} {count:3} consulta(s) {barra}")

    # Distribución de condiciones climáticas
    condiciones = [r["Condicion_Clima"] for r in registros]
    conteo_condiciones = Counter(condiciones)
    print(f"\n  Distribución de condiciones climáticas:")
    print("  " + "-" * 45)
    for condicion, count in conteo_condiciones.most_common():
        porcentaje = round((count / total_consultas) * 100, 1)
        print(f"  • {condicion:<30} {porcentaje:5.1f}%")

    print("  El archivo historial_global.csv está disponible")
    print("     para crear gráficos en Excel o Google Sheets:")
    print("  • Barras:  Consultas por ciudad")
    print("  • Líneas:  Temperatura de una ciudad en el tiempo")
    print("  • Torta:   Distribución de condiciones climáticas")
