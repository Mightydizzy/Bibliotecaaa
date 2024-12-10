import datetime
from src.models.connection import Connection
from src.services.apilibro import APILibro
from src.models.class_client import Client
from src.services.error_log import ErrorLogger 

class PrestamoService:
    def consultar_y_realizar_prestamo(cliente: Client, isbn: str):
        try:
            if isinstance(cliente, dict):
                cliente = Client(
                    id_cliente=cliente.get("id"),
                    nombre=cliente.get("nombre"),
                    email=cliente.get("email"),
                    password=None
                )
            api_libro = APILibro()

            libro = api_libro.obtener_y_guardar_libro_por_isbn(isbn)
            
            if not libro:
                print(f"El libro con ISBN {isbn} no fue encontrado ni en la base de datos ni en la API.")
                return

            print(f"\n--- Detalles del Libro ---")
            print(f"ISBN: {libro.isbn}")
            print(f"Título: {libro.titulo}")
            print(f"Autor: {libro.autor}")
            print(f"Descripción: {libro.descripcion}")
            print(f"Categorías: {libro.categorias}")
            print(f"Número de Páginas: {libro.numero_paginas}")
            print(f"Disponibilidad: {'Sí' if libro.disponibilidad else 'No'}")

            if not libro.disponibilidad:
                print("\nEl libro no está disponible para préstamo.")
                return

            confirmar = input("¿Desea confirmar el préstamo? (s/n): ").strip().lower()
            if confirmar != 's':
                print("\nPréstamo cancelado.")
                return

            with Connection() as db:
                prestamo_query = """
                    INSERT INTO prestamos (usuario_id, isbn, fecha_prestamo)
                    VALUES (%s, (SELECT isbn FROM libros WHERE isbn = %s), %s);
                """
                db.execute_query(prestamo_query, (cliente.id_cliente, isbn, datetime.datetime.now()))

                update_query = "UPDATE libros SET disponibilidad = 0 WHERE isbn = %s;"
                db.execute_query(update_query, (isbn,))

            print(f"\nEl préstamo del libro '{libro.titulo}' ha sido registrado exitosamente para el usuario {cliente.nombre} ({cliente.email}).")
        except Exception as e:
            ErrorLogger.log_error(str(e), module="ModuloPrueba")
            print(f"Error al realizar el préstamo: {e}")