from src.db_connection import conectar_db
from src.utils.hashing import hash_password

class client:
    def __init__(self, id_cliente=None, nombre= None, email=None, password=None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.password = password

    def registrar(self):
        connection = conectar_db()
        if not connection:
            print("No se pudo conectar a la base de datos")
            return
        password_hash = hash_password(self.password)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO usuarios (nombre, email, password_hash)
                VALUES (%s, %s, %s)
                """, (self.nombre, self.email, password_hash))
            connection.commit()
            print("Cliente registrado exitosamente.")
        except Exception as e:
            print(f"Error al registrar cliente: {e}")
        finally:
            connection.close()