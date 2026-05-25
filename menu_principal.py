"""
menu_principal.py - Menú Principal (Post-Login)
Menú de opciones disponibles después de autenticarse.
Organiza las 6 opciones principales de la aplicación.

Desarrollado por: Grupo 56 - ITBA 2026
"""

from clima import consultar_clima_y_guardar, ver_historial_personal
from estadisticas import calcular_estadisticas_globales
from ia_consejos import consejo_vestimenta_ia


def mostrar_acerca_de():
    """
    OPCIÓN 5 DEL MENÚ PRINCIPAL
    Muestra información detallada sobre la aplicación.
    """
    print("ACERCA DE GUARDIÁNCLIMA ITBA")
    print("""
  DESCRIPCIÓN:
          
  GuardiánClima ITBA es una aplicación que
  permite consultar el clima en tiempo real, guardar un historial
  global de consultas, ver estadísticas de uso y obtener consejos
  de vestimenta personalizados mediante Inteligencia Artificial.

  CÓMO USAR CADA OPCIÓN:
  ─────────────────────────────────────────────────────────────
  MENÚ DE ACCESO:
  • Iniciar Sesión:    Ingresá usuario y contraseña registrados.
  • Registrar Usuario: Creá una cuenta con contraseña segura.
  • Salir:             Cierra la aplicación.

  MENÚ PRINCIPAL:
  • Opción 1: Consultá el clima de cualquier ciudad y guardalo.
  • Opción 2: Revisá tu historial personal por ciudad.
  • Opción 3: Estadísticas globales de todos los usuarios.
  • Opción 4: Recibí un consejo de vestimenta con IA Gemini.
  • Opción 5: Esta pantalla de información.
  • Opción 6: Cerrá sesión y volvé al menú de acceso.

  SEGURIDAD Y CONTRASEÑAS:
  ─────────────────────────────────────────────────────────────
  El sistema valida que las contraseñas cumplan:
  ✓ Mínimo 8 caracteres
  ✓ Al menos una MAYÚSCULA y una minúscula
  ✓ Al menos un número
  ✓ Al menos un carácter especial (!@#$%...)

  APIS UTILIZADAS:
  ─────────────────────────────────────────────────────────────
  • OpenWeatherMap: Datos climáticos en tiempo real.
  • Google Gemini:  IA generativa para consejos de vestimenta.

  ARCHIVOS GENERADOS:
  ─────────────────────────────────────────────────────────────
  • usuarios_simulados.csv:  Usuarios registrados.
  • historial_global.csv:    Todas las consultas de clima.
    (Usalo en Excel/Sheets para crear gráficos de barras,
     líneas y torta con los datos globales)

  EQUIPO DE DESARROLLO:
  ─────────────────────────────────────────────────────────────
  Nombre del Grupo: Grupo 56 ITBA 2026

  Integrantes:
  • Juliana Guillen
  • Jose Francisco Grassi
  • Fernando Ariel Seisdedos
    """)


def menu_principal(username):
    """
    Menú principal de la aplicación (post-login).
    Permite acceder a todas las funcionalidades principales.
    Retorna cuando el usuario cierra sesión (opción 6).
    
    Parámetro:
    - username: usuario autenticado que usa la aplicación
    """
    ultima_consulta_sesion = None  # Guarda la última consulta para uso en IA

    while True:
        print(f"\n GuardiánClima ITBA  |  Usuario: {username}")
        print("  1. Consultar Clima Actual y Guardar en Historial")
        print("  2. Ver Mi Historial Personal por Ciudad")
        print("  3. Estadísticas Globales de Uso")
        print("  4. Consejo IA: ¿Cómo Me Visto Hoy?")
        print("  5. Acerca De...")
        print("  6. Cerrar Sesión")

        opcion = input("\nElegí una opción (1-6): ").strip()

        if opcion == '1':
            # Opción 1: Consultar clima y guardar en historial
            datos = consultar_clima_y_guardar(username)
            if datos:
                # Guardar para usar en opción 4 (IA)
                ultima_consulta_sesion = datos

        elif opcion == '2':
            # Opción 2: Ver historial personal del usuario
            ver_historial_personal(username)

        elif opcion == '3':
            # Opción 3: Estadísticas globales de todos los usuarios
            calcular_estadisticas_globales()

        elif opcion == '4':
            # Opción 4: Consejo de vestimenta con IA
            consejo_vestimenta_ia(username, ultima_consulta_sesion)

        elif opcion == '5':
            # Opción 5: Información sobre la aplicación
            mostrar_acerca_de()

        elif opcion == '6':
            # Opción 6: Cerrar sesión y volver al menú de acceso
            print(f"\n ¡Hasta luego, {username}! Sesión cerrada.")
            break

        else:
            print("Opción inválida. Ingresá un número del 1 al 6.")

        input("\n  Presioná Enter para continuar...")
