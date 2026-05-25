"""
gestion_usuarios.py - Gestión Simulada de Usuarios
Maneja registro, login y almacenamiento de usuarios en CSV.

Desarrollado por: Grupo 56 - ITBA 2026
"""

import csv
import os
from config import ARCHIVO_USUARIOS
from validacion_password import validar_password, mostrar_feedback_password


def inicializar_archivo_usuarios():
    """Crea el archivo CSV de usuarios si no existe."""
    if not os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password_simulada"])


def cargar_usuarios():
    """
    Carga todos los usuarios desde el CSV.
    
    Retorna:
    - dict {username: password_simulada}
    """
    inicializar_archivo_usuarios()
    usuarios = {}
    try:
        with open(ARCHIVO_USUARIOS, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for fila in reader:
                usuarios[fila["username"]] = fila["password_simulada"]
    except FileNotFoundError:
        pass
    return usuarios


def guardar_usuario(username, password):
    """
    Agrega un nuevo usuario al archivo CSV de usuarios.
    
    Parámetros:
    - username: nombre de usuario a registrar
    - password: contraseña (ya validada)
    """
    inicializar_archivo_usuarios()
    with open(ARCHIVO_USUARIOS, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([username, password])


def registrar_usuario():
    """
    Proceso completo de registro de un nuevo usuario.
    
    Flujo:
    1. Solicita nombre de usuario (validar que no exista)
    2. Solicita contraseña (con validación de requisitos)
    3. Solicita confirmación de contraseña
    4. Guarda el usuario en CSV
    
    Retorna:
    - username si el registro fue exitoso
    - None si el usuario canceló
    """

    print("REGISTRO DE NUEVO USUARIO")

    # ===== PASO 1: Obtener nombre de usuario =====
    while True:
        username = input("\nIngresá tu nombre de usuario (o 'cancelar' para volver): ").strip()

        if username.lower() == 'cancelar':
            return None

        if not username:
            print("El nombre de usuario no puede estar vacío.")
            continue

        # Verificar si el usuario ya existe
        usuarios = cargar_usuarios()
        if username in usuarios:
            print(f"El usuario '{username}' ya existe. Elegí otro nombre.")
            continue

        break

    # ===== PASO 2: Validar y obtener contraseña =====
    while True:
        print(f"\nUsuario '{username}' disponible ")
        print("\n Requisitos de contraseña:")
        print("   • Mínimo 8 caracteres")
        print("   • Al menos una MAYÚSCULA")
        print("   • Al menos una minúscula")
        print("   • Al menos un número")
        print("   • Al menos un carácter especial (!@#$%^&*...)")

        password = input("\nIngresá tu contraseña: ").strip()

        if not password:
            print("La contraseña no puede estar vacía.")
            continue

        # Validar la contraseña contra todos los requisitos
        es_valida, reglas_incumplidas = validar_password(password)

        if not es_valida:
            # Si la contraseña no cumple, mostrar feedback
            mostrar_feedback_password(reglas_incumplidas)
            opcion = input("\n¿Querés intentar con otra contraseña? (s/n): ").strip().lower()
            if opcion != 's':
                return None
            continue

        # ===== PASO 3: Confirmar contraseña =====
        confirmacion = input("Confirmá tu contraseña: ").strip()
        if password != confirmacion:
            print("Las contraseñas no coinciden. Intentá de nuevo.")
            continue

        # ===== PASO 4: Guardar usuario =====
        guardar_usuario(username, password)
        print(f"\n ¡Usuario '{username}' registrado exitosamente!")
        return username


def iniciar_sesion():
    """
    Proceso de inicio de sesión.
    Permite 3 intentos antes de rechazar el acceso.
    
    Retorna:
    - username si el login fue exitoso
    - None si falló después de 3 intentos
    """

    print("INICIAR SESIÓN")

    intentos = 3
    while intentos > 0:
        username = input("\nNombre de usuario: ").strip()
        password = input("Contraseña: ").strip()

        usuarios = cargar_usuarios()

        # Verificar credenciales
        if username in usuarios and usuarios[username] == password:
            print(f"\n ¡Bienvenido, {username}!")
            return username
        else:
            intentos -= 1
            if intentos > 0:
                print(f"Credenciales incorrectas. Te quedan {intentos} intento(s).")
            else:
                print("Demasiados intentos fallidos. Volviendo al menú de acceso.")

    return None
