from src.models.libro import Libro
from src.services.api_client import APIClient
from src.services.db_libro import DBLibro
from src.services.error_log import ErrorLogger 
class APILibro:

    def __init__(self):
        self.api_client = APIClient()
        self.db_repo = DBLibro()


    def obtener_libros_sin_repetir(self):
        try:
            libros_api = self.api_client.get("libros")
        except ValueError as e:
            ErrorLogger.log_error(str(e), module="Obtener libros api")
            print(f"Error al obtener libros de la API: {e}")
            libros_api = []
        
        libros_db = self.db_repo.obtener_todos_los_libros()
        
        libros_unicos = {libro["isbn"]: libro for libro in libros_api}
        for libro_db in libros_db:
            libros_unicos[libro_db[0]] = {
                "isbn": libro_db[0],
                "titulo": libro_db[1],
                "autor": libro_db[2],
                "descripcion": libro_db[3],
                "categorias": libro_db[4],
                "numero_paginas": libro_db[5],
                "disponibilidad": libro_db[6],
            }
        return list(libros_unicos.values())
 
    def obtener_y_guardar_libro_por_isbn(self, isbn: str)-> dict:
        try:
        # Revisa si el libro ya está en la base de datos
            libro_db = self.db_repo.buscar_libro_por_isbn(isbn)
            if libro_db:
            # Convierte la tupla de la base de datos en una instancia de Libro
                return Libro(
                    isbn=libro_db[0],
                    titulo=libro_db[1],
                    autor=libro_db[2],
                    descripcion=libro_db[3],
                    categorias=libro_db[4],
                    numero_paginas=libro_db[5],
                    disponibilidad=libro_db[6],
            )
        except Exception as e:
            ErrorLogger.log_error(str(e), module="Api libro")
            print(f"Hubo un problema al consultar la base de datos: {e}")

        # Si no está en la base de datos, busca en la API
            libro_data = self.api_client.get(f"libros/{isbn}")
            libro = Libro.from_dict(libro_data)

        # Guarda el libro en la base de datos
            self.db_repo.guardar_libro(libro)

            return libro
        except Exception as e:
            ErrorLogger.log_error(str(e), module="Api libro")
            print(f"Error al obtener libro por ISBN: {e}")
        return None
 
