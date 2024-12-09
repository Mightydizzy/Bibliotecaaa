from src.services.apilibro import APILibro
from src.models.class_client import Client
from src.repo.client_repository import ClientRepository
from src.models.validator import validator
from src.client.auth_service import AuthService
from src.services.prestamo_service import PrestamoService
from src.models.db_libro import DBLibro
from src.models.libro import Libro
import getpass
api_libro = APILibro()
db_libro = DBLibro()

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
            print("2. Buscar libros por ISBN")
            print("3. Realizar un préstamo")
            print("4. Cerrar sesión")
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
                password = getpass.getpass("Ingresa tu contraseña con al menos 7 caracteres, una mayúscula y un número: ").strip()

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
                password = getpass.getpass("Ingresa tu contraseña: ").strip()

                auth_service = AuthService()
                usuario_actual = auth_service.authenticate_client(email, password)

                if usuario_actual:
                    print_separator()
                    print(r"""   *  .  . *       *    .        .        .   *    ..
 .    *        .   ###     .      .        .            *
    *.   *        #####   .     *      *        *    .
  ____       *  ######### *    .  *      .        .  *   .
 /   /\  .     ###\#|#/###   ..    *    .      *  .  ..  *
/___/  ^8/      ###\|/###  *    *            .      *   *
|   ||%%(        # )|(  #
|___|,  \\          )|(""")
                    print_separator()
                    print(f"Bienvenido, {usuario_actual['nombre']}!")
                else:
                    print("Error en la autenticación. Verifica tus credenciales.")
            except Exception as e:
                print(f"Error al autenticar: {e}")

       
        elif usuario_actual and opcion == "1": 
            #TODO mostrar todos los libros
            print("\nMostrando todos los libros disponibles...")
            libros = api_libro.obtener_libros_sin_repetir()
            if libros:
                for libro in libros:
                    print(f"ISBN: {libro['isbn']}, Título: {libro['titulo']}, Autor: {libro['autor']}")
            else:
                print("\nNo se encontraron libros disponibles.")
        
        elif usuario_actual and opcion == "2":
            isbn = input("Ingrese el ISBN del libro: ").strip()
            print(f"Buscando libro con ISBN {isbn}...")
            libro = api_libro.obtener_y_guardar_libro_por_isbn(isbn)
    
            if libro:
                print("\n--- Detalles del Libro ---")
                # Usa los atributos de la instancia de `Libro`
                print(f"ISBN: {libro.isbn}")
                print(f"Título: {libro.titulo}")
                print(f"Autor: {libro.autor}")
                print(f"Descripción: {libro.descripcion}")
                print(f"Categorías: {libro.categorias}")
                print(f"Número de Páginas: {libro.numero_paginas}")
                print(f"Disponibilidad: {'Sí' if libro.disponibilidad else 'No'}")
            else:
                print("\nEl libro no fue encontrado en la API ni en la base de datos.")


        elif usuario_actual and opcion == "3":
            isbn = input("Ingrese el ISBN del libro que desea prestar: ").strip()
            PrestamoService.consultar_y_realizar_prestamo(usuario_actual, isbn)


        elif usuario_actual and opcion == "4":
            # Cerrar sesión
            print(f"Hasta luego, {usuario_actual.nombre}!")
            usuario_actual = None

        elif opcion == "3" and not usuario_actual or opcion == "4" and usuario_actual:
            # Salir del sistema
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida, intenta nuevamente.")

if __name__ == "__main__":
    main()
