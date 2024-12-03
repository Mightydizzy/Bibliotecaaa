from src.models.class_client import client
from src.db_connection import conectar_db

def main():
    while True:
        print("\n--- Sistema de Registro de Usuarios ---")
        print("1. Registrar un nuevo usuario")
        print("2. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nombre = input("Ingresa tu nombre: ").strip()
            email = input("Ingresa tu email: ").strip()
            password = input("Ingresa tu contraseña: ").strip()

            cliente = client(nombre=nombre, email=email, password=password)
            cliente.registrar()

            if not nombre or not email or not password:
                print("Todos los campos son obligatorios.")
                continue
            
        elif opcion == "2":
            print("Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida, intenta nuevamente.")

if __name__ == "__main__":
    main()