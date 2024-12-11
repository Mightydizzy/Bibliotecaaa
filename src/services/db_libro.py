from src.models.connection import Connection
from src.models.libro import Libro
from src.services.error_log import ErrorLogger 

class DBLibro:

    @staticmethod
    def obtener_todos_los_libros():
        query =  "SELECT isbn, titulo, autor, descripcion, categorias, numero_paginas, disponibilidad FROM libros"
        with Connection() as db:
            return db.execute_query(query).fetchall()

    @staticmethod
    def guardar_libro(libro: Libro):
        query = """
        INSERT INTO libros (isbn, titulo, autor, descripcion, categorias, numero_paginas, disponibilidad)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            titulo = VALUES(titulo),
            autor = VALUES(autor),
            descripcion = VALUES(descripcion),
            categorias = VALUES(categorias),
            numero_paginas = VALUES(numero_paginas),
            disponibilidad = VALUES(disponibilidad);
        """
        try:
            # Ejecutar la consulta
            with Connection() as db:
                db.execute_query(query, (
                    libro.isbn,
                    libro.titulo,
                    libro.autor,
                    libro.descripcion,
                    libro.categorias,
                    libro.numero_paginas,
                    libro.disponibilidad
                ))
        
        except Exception as e:
            ErrorLogger.log_error(str(e), module="Módulo Guardar Libro")
            print(f"Error al guardar el libro: {e}")

    @staticmethod
    def buscar_libro_por_isbn(isbn):
        query = "SELECT * FROM libros WHERE isbn = %s;"
        with Connection() as db:
            cursor = db.execute_query(query, (isbn,))
            return cursor.fetchone()
        
    @staticmethod
    def crear_libro(isbn, titulo, autor, descripcion, categorias, numero_paginas, disponibilidad):
        query = """
        INSERT INTO libros (isbn, titulo, autor, descripcion, categorias, numero_paginas, disponibilidad)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            # Ejecutar la consulta
            with Connection() as db:
                db.execute_query(query, (isbn, titulo, autor, descripcion, categorias, numero_paginas, disponibilidad))
            print("Libro agregado correctamente.")
        except Exception as e:
            ErrorLogger.log_error(str(e), module="Módulo crear libro")
            print(f"Error al crear el libro: {e}")

    @staticmethod
    def ver_libros():
        query = "SELECT * FROM libros"
        with Connection() as db:
            cursor = db.execute_query(query)
            return cursor.fetchall()

    @staticmethod
    def editar_libro(book_id, isbn=None, titulo=None, autor=None, descripcion=None, categorias=None, numero_paginas=None, disponibilidad=None):
        fields = []
        values = []

        if isbn:
            fields.append("isbn = %s")
            values.append(isbn)
        if titulo:
            fields.append("titulo = %s")
            values.append(titulo)
        if autor:
            fields.append("autor = %s")
            values.append(autor)
        if descripcion:
            fields.append("descripcion = %s")
            values.append(descripcion)
        if categorias:
            fields.append("categorias = %s")
            values.append(categorias)
        if numero_paginas:
            fields.append("numero_paginas = %s")
            values.append(numero_paginas)
        if disponibilidad is not None:
            fields.append("disponibilidad = %s")
            values.append(disponibilidad)

        query = f"UPDATE libros SET {', '.join(fields)} WHERE isbn = %s"
        values.append(book_id)

        try:
            with Connection() as db:
                db.execute_query(query, tuple(values))  # No es necesario el commit explícito
            print("Libro actualizado correctamente.")
        except Exception as e:
            ErrorLogger.log_error(str(e), module="Módulo Editar Libro")
            print(f"Error al editar el libro: {e}")



    @staticmethod
    def eliminar_libro(isbn):
        query_buscar = "SELECT * FROM libros WHERE isbn = %s"
        query_eliminar = "DELETE FROM libros WHERE isbn = %s"
        
        try:
            with Connection() as db:
                libro = db.execute_query(query_buscar, (isbn,)).fetchone()
                
                if not libro:
                    print(f"No se encontró un libro con el ISBN {isbn}.")
                    return
                # muestra los detalles
                print("\n--- Detalles del Libro ---")
                print(f"ISBN: {libro[0]}")
                print(f"Título: {libro[1]}")
                print(f"Autor: {libro[2]}")
                print(f"Descripción: {libro[3]}")
                print(f"Categorías: {libro[4]}")
                print(f"Número de Páginas: {libro[5]}")
                print(f"Disponibilidad: {'Sí' if libro[6] else 'No'}")
                
                # confirmación
                confirmar = input("\n¿Desea confirmar la eliminación del libro? (s/n): ").strip().lower()
                if confirmar != 's':
                    print("Eliminación cancelada.")
                    return
                
                # eliminación
                db.execute_query(query_eliminar, (isbn,))
                print(f"\nEl libro con ISBN {isbn} ha sido eliminado exitosamente.")
        
        except Exception as e:
            ErrorLogger.log_error(str(e), module="ModuloEliminarLibro")
            print(f"Error al eliminar el libro: {e}")
