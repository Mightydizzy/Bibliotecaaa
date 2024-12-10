from src.models.validator import validator
from src.utils.hashing import hash_password
from src.models.class_client import Client
from src.models.connection import Connection
from src.services.error_log import ErrorLogger 

class ClientRepository:
    def registrar(self, client: Client):
        try:
            validator.validar_cliente(client)
            password_hash = hash_password(client.password)
            with Connection() as db:
                sql = """
                    INSERT INTO usuarios (nombre, email, password_hash)
                    VALUES (%s, %s, %s)
                """
                db.execute_query(sql, (client.nombre, client.email, password_hash))
            
            print("Usuario registrado exitosamente.")
            return True

        except ValueError as ve:
            ErrorLogger.log_error(str(ve), module="ModuloPrueba")
            print(f"Error de validación: {ve}")
        except Exception as e:
            print(f"Error inesperado al registrar usuario: {str(e)}")
            ErrorLogger.log_error(str(e), module="ModuloPrueba")
        return False