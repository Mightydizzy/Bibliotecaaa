from datetime import datetime
from src.models.connection import Connection
from src.services.apilibro import APILibro
from src.models.class_client import Client
from src.services.error_log import ErrorLogger 
from src.models.prestamo import Prestamo

class PrestamoService:
    
    @classmethod
    def consultar_y_realizar_prestamo(self, cliente: Client, isbn: str):
        try:  
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

            confirmar = input("¿Desea confirmar la solicitud de préstamo? (s/n): ").strip().lower()
            if confirmar != 's':
                print("\nPréstamo cancelado.")
                return
            prestamo = Prestamo(cliente=cliente, libro=libro)

            with Connection() as db:
                prestamo_query = """INSERT INTO prestamos (usuario_id, isbn, fecha_prestamo)
                    VALUES (%s, (SELECT isbn FROM libros WHERE isbn = %s), %s);"""
                db.execute_query(prestamo_query, (prestamo.cliente.id_cliente, prestamo.libro.isbn, prestamo.fecha_prestamo))

                update_query = "UPDATE libros SET disponibilidad = 0 WHERE isbn = %s;"
                db.execute_query(update_query, (isbn,))
                select_id_query = """ SELECT id FROM prestamos
                    WHERE usuario_id = %s AND isbn = %s
                    ORDER BY fecha_prestamo DESC LIMIT 1; """
                cursor = db.execute_query(select_id_query, (cliente.id_cliente, libro.isbn))
                prestamo_id = cursor.fetchone()[0]

            print(f"\nEl préstamo con ID '{prestamo_id}' del libro '{libro.titulo}' ha sido registrado exitosamente para el usuario {cliente.nombre} ({cliente.email}).")
        except Exception as e:
            ErrorLogger.log_error(str(e), module="Módulo solicitar préstamo.")
            print(f"Error al realizar el préstamo: {e}")


    @staticmethod
    def devolver_prestamo(prestamo_id: int):
        try:
            with Connection() as db:
                # Fetch detalles del prestamo
                query = """ SELECT prestamos.id, libros.titulo, libros.autor, prestamos.fecha_prestamo, prestamos.fecha_devolucion
                    FROM prestamos
                    JOIN libros ON prestamos.isbn = libros.isbn
                    WHERE prestamos.id = %s; """
                cursor = db.execute_query(query, (prestamo_id,))
                prestamo = cursor.fetchone()

                if not prestamo:
                    print(f"No se encontró un préstamo con ID {prestamo_id}.")
                    return

                # Unpack detalles del prestamo
                prestamo_id, titulo, autor, fecha_prestamo, fecha_devolucion = prestamo
            
                # mostrar detalles del libro y préstamo
                print("\n--- Detalles del Préstamo ---")
                print(f"ID del Préstamo: {prestamo_id}")
                print(f"Título del Libro: {titulo}")
                print(f"Autor: {autor}")
                print(f"Fecha de Préstamo: {fecha_prestamo.strftime('%Y-%m-%d')}")
                print(f"Estado: {'Devuelto' if fecha_devolucion else 'Pendiente'}")
                
                # Confirm return
                confirmar = input("\n¿Desea confirmar la devolución de este libro? (s/n): ").strip().lower()
                if confirmar != 's':
                    print("\nDevolución cancelada.")
                    return

                # actualizar log de prestamo y disp del libro
                update_prestamo_query = """ UPDATE prestamos
                    SET fecha_devolucion = %s
                    WHERE id = %s; """
                update_libro_query = """ UPDATE libros
                    SET disponibilidad = 1
                    WHERE isbn = (SELECT isbn FROM prestamos WHERE id = %s); """
                fecha_actual = datetime.now()
                db.execute_query(update_prestamo_query, (fecha_actual, prestamo_id))
                db.execute_query(update_libro_query, (prestamo_id,))

                print(f"\nEl libro '{prestamo[1]}' ha sido devuelto exitosamente.")

        except Exception as e:
            ErrorLogger.log_error(str(e), module="Devolver Préstamo")
            print(f"Error al devolver el libro: {e}")


    @staticmethod
    def listar_prestamos_usuario(usuario_id: int):
        try:
            with Connection() as db:
                query = """ SELECT prestamos.id, libros.titulo, prestamos.fecha_prestamo, prestamos.fecha_devolucion
                    FROM prestamos
                    JOIN libros ON prestamos.isbn = libros.isbn
                    WHERE prestamos.usuario_id = %s
                    ORDER BY prestamos.fecha_prestamo DESC
                    LIMIT 10; """
                prestamos = db.execute_query(query, (usuario_id,))

            if not prestamos:
                print("\nNo se encontraron préstamos para este usuario.")
                return

            print("\n--- Últimos 10 préstamos ---")
            for prestamo in prestamos:
                estado = "Devuelto" if prestamo[3] else "Pendiente"
                print(f"ID: {prestamo[0]}, Título: {prestamo[1]}, Fecha Préstamo: {prestamo[2].strftime('%Y-%m-%d')}, Estado: {estado}")
        except Exception as e:
            ErrorLogger.log_error(str(e), module="Consultar Préstamos")
            print(f"Error al listar los préstamos: {e}")