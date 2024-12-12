from src.services.apilibro import APILibro
from src.models.class_client import Client
from src.repo.client_repository import ClientRepository
from src.models.validator import validator
from src.client.auth_service import AuthService
from src.services.prestamo_service import PrestamoService
from src.services.db_libro import DBLibro
from src.models.connection import Connection
import getpass
from src.services.error_log import ErrorLogger
api_libro = APILibro()
db_libro = DBLibro()

def print_separator():
    """Imprime una línea separadora para mejorar la legibilidad del menú."""
    print("\n" + "-" * 70 + "\n")

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
    try:

        while True:
            if usuario_actual:
                print("\nOpciones:")
                print("1. Visualizar todos los libros")
                print("2. Buscar libros por ISBN")
                print("3. Solicitar un préstamo de libro")
                print("4. Consultar préstamo")
                print("5. Devolver libro")
                print("6. Agregar libro")
                print("7. Editar libro")
                print("8. Eliminar libro")
                print("9. Cerrar sesión")
                print("10. Salir del sistema")
            
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
                    print(f"usuario: {nombre},correo {email}")

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
    .    *        .    ###     .      .        .            *
        *.   *        #####   .     *      *        *    .
      ___       *   ######### *    .  *      .        .  *   .
     /  /\  .      ###\#|#/###   ..    *    .      *  .  ..  *
    /___/ \         ###\|/###  *    *            .      *   *
    |   |||          # )|(  #
    |___|,|            )|(""")
                        print_separator()
                        if isinstance(usuario_actual, dict):
                            nombre = usuario_actual["nombre"]
                        else:
                            nombre = usuario_actual.nombre

                        print(f"Bienvenido, {nombre}!")

                        print(f"Bienvenido, {usuario_actual['nombre']}!")
                    else:
                        print("Error en la autenticación. Verifica tus credenciales.")
                except Exception as e:
                    ErrorLogger.log_error(str(e), module="main")
        
            elif usuario_actual and opcion == "1": 
                print_separator()
                print("\nMostrando todos los libros disponibles...")
                print_separator()
                libros = api_libro.obtener_libros_sin_repetir()
                if libros:
                    for libro in libros:
                        print(f"ISBN: {libro['isbn']}, Título: {libro['titulo']}, Autor: {libro['autor']}")
                        
                    print_separator()    
                else:
                    print("\nNo se encontraron libros disponibles.")
                    print_separator()
            
            elif usuario_actual and opcion == "2":
                print_separator()
                isbn = input("Ingrese el ISBN del libro: ").strip()
                print(f"Buscando libro con ISBN {isbn}...")
                libro = api_libro.obtener_y_guardar_libro_por_isbn(isbn)
                print_separator()
        
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
                    print_separator()
                else:
                    print_separator()
                    print("\nEl libro no fue encontrado en la API ni en la base de datos.")
                    print_separator()


            elif usuario_actual and opcion == "3":
                print_separator()
                isbn = input("Ingrese el ISBN del libro que desea solicitar: ").strip()
                PrestamoService.consultar_y_realizar_prestamo(usuario_actual, isbn)
                print_separator()

            elif usuario_actual and opcion == "4":
                print_separator()
                PrestamoService.listar_prestamos_usuario(usuario_actual.id_cliente)
                print_separator()

            elif usuario_actual and opcion == "5":
                try:
                    prestamo_id = int(input("Ingrese el ID del préstamo que desea devolver: ").strip())
                    PrestamoService.devolver_prestamo(prestamo_id)
                    print_separator()
                except ValueError:
                    print("ID de préstamo inválido. Debe ser un número.")


            elif usuario_actual and opcion == "6":
                # Crear un nuevo libro
                print("\nCrear un nuevo libro:")
                isbn = input("ISBN: ").strip()
                titulo = input("Título: ").strip()
                autor = input("Autor: ").strip()
                descripcion = input("Descripción: ").strip()
                categorias = input("Categorías: ").strip()
                numero_paginas = input("Número de páginas: ").strip()
                disponibilidad = input("Disponibilidad (1 para disponible, 0 para no disponible): ").strip()

                db_libro.crear_libro(isbn, titulo, autor, descripcion, categorias, numero_paginas, disponibilidad)


            elif usuario_actual and opcion == "7":
                # Editar un libro
                isbn = input("Ingrese el ISBN del libro a editar: ").strip()
                libro = db_libro.buscar_libro_por_isbn(isbn)

                if libro:
                    print("\nIngrese los nuevos detalles del libro (deje vacío para no cambiar):")
                    nuevo_isbn = input(f"Nuevo ISBN ({libro[0]}): ").strip() or libro[0]
                    nuevo_titulo = input(f"Nuevo Título ({libro[1]}): ").strip() or libro[1]
                    nuevo_autor = input(f"Nuevo Autor ({libro[2]}): ").strip() or libro[2]
                    nueva_descripcion = input(f"Nuevo Descripción ({libro[3]}): ").strip() or libro[3]
                    nuevas_categorias = input(f"Nuevas Categorías ({libro[4]}): ").strip() or libro[4]
                    nuevo_numero_paginas = input(f"Nuevo Número de Páginas ({libro[5]}): ").strip() or libro[5]
                    nueva_disponibilidad = input(f"Nueva Disponibilidad ({'Sí' if libro[6] else 'No'}): ").strip() or libro[6]

                    db_libro.editar_libro(libro[0], nuevo_isbn, nuevo_titulo, nuevo_autor, nueva_descripcion, nuevas_categorias, nuevo_numero_paginas, nueva_disponibilidad)

            elif usuario_actual and opcion == "8":
                # Eliminar un libro
                isbn = input("Ingrese el ISBN del libro a eliminar: ").strip()
                db_libro.eliminar_libro(isbn)

            elif usuario_actual and opcion == "9":
                print(f"Cerrando sesión de {usuario_actual.nombre}...")
                usuario_actual = None  # Reinicia el estado de sesión
                print("Has cerrado sesión correctamente.")

            elif opcion == "3" and not usuario_actual or opcion == "10" and usuario_actual:
                # Salir del sistema
                print("Saliendo del sistema...")
                
                break

            else:
                print("Opción inválida, intenta nuevamente.")
    finally:
        Connection.close
        print("Conexión cerrada correctamente.")
        
    

if __name__ == "__main__":
    main()
