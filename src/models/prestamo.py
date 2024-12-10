from datetime import datetime
from src.models.libro import Libro
from src.models.class_client import Client

class Prestamo:

    def __init__(self,  cliente: Client, libro: Libro, fecha_prestamo: datetime = None, prestamo_id: int = None, fecha_devolucion: datetime = None):
        self.prestamo_id = prestamo_id
        self.cliente = cliente
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo if fecha_prestamo else datetime.now()
        self.fecha_devolucion = fecha_devolucion


    def to_dict(self) -> dict:
        return {
            "id_cliente": self.cliente.id_cliente,
            "nombre_cliente": self.cliente.nombre,
            "email_cliente": self.cliente.email,
            "isbn_libro": self.libro.isbn,
            "titulo_libro": self.libro.titulo,
            "fecha_prestamo": self.fecha_prestamo.isoformat(),
            "fecha_devolucion": self.fecha_devolucion.isoformat() if self.fecha_devolucion else None
        }
