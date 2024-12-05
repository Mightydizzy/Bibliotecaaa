
from src.models.class_client import Client
from src.models.client_repository import ClientRepository
from src.models.validator import validator
from src.client.auth_service import AuthService


def print_separator():
    """Imprime una línea separadora para mejorar la legibilidad del menú."""
    print("\n" + "-" * 50 + "\n")

def main():
    print("        ╭══• ೋ•✧๑-ˋˏ ༻✿༺ ˎˊ-๑✧•ೋ •══╮")
    print("       - Bienvenido a la biblioteca -")
    print("        ╰══• ೋ•✧๑-ˋˏ ༻✿༺ ˎˊ-๑✧•ೋ •══╯")
    print(r"""     
     __...--~~~~~-._   _.-~~~~~--...__
    //               `V'               \\ 
   //                 |                 \\ 
  //__...--~~~~~~-._  |  _.-~~~~~~--...__\\ 
 //__.....----~~~~._\ | /_.~~~~----.....__\\
====================\\|//====================
                    `---`""")
    print("✧･ﾟ:* Para solicitar un préstamo debes iniciar sesión *:･ﾟ✧")
    usuario_actual = None  

    while True:
        if usuario_actual:
            print("\nOpciones:")
            print("1. Visualizar todos los libros")
            print("2. Buscar libros por autor")
            print("3. Buscar libros por ISBN")
            print("4. Realizar un préstamo")
            print("5. Cerrar sesión")
        else:
            print("\nOpciones:")
            print("1. Registrar un nuevo usuario")
            print("2. Iniciar sesión")
            print("3. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1" and not usuario_actual:

            try:
                nombre = input("Ingresa tu nombre: ").strip()
                email = input("Ingresa tu email: ").strip()
                password = input("Ingresa tu contraseña con al menos 7 caracteres, una mayúscula y un número: ").strip()

                validator.validar_email(email)
                validator.validar_password(password)

                cliente = Client(nombre=nombre, email=email, password=password)
                repo = ClientRepository()
                repo.registrar(cliente)
            except ValueError as ve:
                print(f"Error de validación: {ve}")
            except Exception as e:
                print(f"Error inesperado: {e}")

        elif opcion == "2" and not usuario_actual:
            try:
                email = input("Ingresa tu email: ").strip()
                password = input("Ingresa tu contraseña: ").strip()

                auth_service = AuthService()
                usuario_actual = auth_service.authenticate_client(email, password)

                if usuario_actual:
                    print(f"Bienvenido, {usuario_actual['nombre']}!")
                else:
                    print("Error en la autenticación. Verifica tus credenciales.")
            except Exception as e:
                print(f"Error al autenticar: {e}")

       
        elif usuario_actual and opcion == "1": 
            #TODO mostrar todos los libros
            print("la visualización de todos los libros está en desarrollo. Por favor, intente más tarde.")
        
        elif usuario_actual and opcion == "2":
            #TODO Buscar libros por autor (en desarrollo)
            print("La búsqueda de libros por autor está en desarrollo. Por favor, intente más tarde.")
        
        elif usuario_actual and opcion == "3":
            #TODO Buscar libros por ISBN (en desarrollo)
            print("La búsqueda de libros por ISBN está en desarrollo. Por favor, intente más tarde.")

        elif usuario_actual and opcion == "4":
            #TODO Realizar préstamo (en desarrollo)
            print("La funcionalidad de realizar préstamos está en desarrollo. Por favor, intente más tarde.")

        elif usuario_actual and opcion == "5":
            # Cerrar sesión
            print(f"Hasta luego, {usuario_actual['nombre']}!")
            usuario_actual = None

        elif opcion == "3" and not usuario_actual or opcion == "5" and usuario_actual:
            # Salir del sistema
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida, intenta nuevamente.")

if __name__ == "__main__":
    main()
