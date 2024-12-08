from src.models.connection import Connection
from src.models.libro import Libro

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
            print(f"Error al guardar el libro: {e}")

    @staticmethod
    def buscar_libro_por_isbn(isbn):
        query = "SELECT * FROM libros WHERE isbn = %s;"
        with Connection() as db:
            cursor = db.execute_query(query, (isbn,))
            return cursor.fetchone()
