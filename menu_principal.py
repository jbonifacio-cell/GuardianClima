"""
menu_acceso.py - Menú de Acceso (Pre-Login)
Maneja el login, registro y salida.
"""

from gestion_usuarios import iniciar_sesion, registrar_usuario
from menu_principal import menu_principal


def menu_acceso():
    """
    Muestra el menú de acceso y gestiona login/registro.

    """
    while True:
        print("\n" + "=" * 50)
        print("GuardiánClima ITBA")
        print("  1. Iniciar Sesión")
        print("  2. Registrar Nuevo Usuario")
        print("  3. Salir")

        opcion = input("\nElegí una opción (1-3): ").strip()

        if opcion == '1':
            username = iniciar_sesion()
            if username:
                menu_principal(username)

        elif opcion == '2':
            username = registrar_usuario()
            if username:
                print(f"\n ¡Registro exitoso! Entrando al menú principal...")
                menu_principal(username)

        elif opcion == '3':
            print("\n ¡Hasta luego! Gracias por usar GuardiánClima ITBA.")
            break

        else:
            print("Opción inválida. Ingresá 1, 2 o 3.")
