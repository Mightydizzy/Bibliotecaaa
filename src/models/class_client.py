from src.db_connection import conectar_db
from src.utils.hashing import hash_password
import re
class client:
    def __init__(self, id_cliente=None, nombre= None, email=None, password=None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.password = password

    def validar_email(self):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not isinstance(self.email, str) or not self.email:
            raise ValueError("El email proporcionado debe ser una cadena no vacía.")
        
        if not re.match(email_regex, self.email):
            raise ValueError("El email no tiene un formato válido. Ejemplo válido: usuario@dominio.com.")
        connection = conectar_db()
        if not connection: 
            raise ConnectionError("No se pudo conectar a la base de datos para validar el email.")
        try: 
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = %s", (self.email,))
                resultado = cursor.fetchone()
                if resultado[0] > 0:
                    raise ValueError(f"El email '{self.email}' ya está registrado.")
        except Exception as e:
            raise ValueError(f"Error al verificar el email: {e}")
        finally: 
            if connection:
                connection.close()
    
    def validate_password (self):
        if len(self.password) < 7:
            return False
        if not any(char.isdigit() for char in self.password):
            return False
        if not any(char.isupper() for char in self.password):
            return False
        return True

    def registrar(self):
        try: 
            self.validar_email()
            if not self.validate_password():
                raise ValueError ("La contraseña debe tener al menos 7 caracteres, incluir un número y una letra mayúscula.")
            connection = conectar_db()
            if not connection:
                print("No se pudo conectar a la base de datos")
            password_hash = hash_password(self.password)
            with connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO usuarios (nombre, email, password_hash)
                VALUES (%s, %s, %s)
                """, (self.nombre, self.email, password_hash))
            connection.commit()
            print("Cliente registrado exitosamente.")
        except ValueError as ve:
            print(f"Error de validación: {ve}")
        except ConnectionError as ce:
            print(f"Error de conexión: {ce}")
        except Exception as e:
            print(f"Error inesperado al registrar cliente: {e}")
        finally:
            if 'connection' in locals() and connection:
                connection.close()