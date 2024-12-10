import re
from src.models.connection import Connection
from src.models.class_client import Client
from src.services.error_log import ErrorLogger 

class validator:

    @staticmethod
    def validar_email(email: str):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not isinstance(email, str) or not email:
            raise ValueError("El email proporcionado debe ser una cadena no vacía.")
        if not re.match(email_regex, email):
            raise ValueError("El email no tiene un formato válido. Ejemplo válido: usuario@dominio.com.")
        
    @staticmethod
    def validar_email_duplicado(email: str)-> bool:
        try: 
            with Connection() as db:
                cursor = db.execute_query("SELECT COUNT(*) FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone()[0] > 0:
                raise ValueError(f"El email '{email}' ya está registrado.")
        except Exception as e:
            ErrorLogger.log_error(str(e), module="validator")
            raise ValueError(f"Error al verificar el email: {e}")
        return True

    
    @staticmethod
    def validar_password (password: str)-> bool:
        if len(password) < 7:
            raise ValueError("La contraseña debe tener al menos 7 carácteres.")
        if not any(char.isdigit() for char in password):
            raise ValueError("La contraseña debe incluir al menos un número.")
        if not any(char.isupper() for char in password):
            raise ValueError("La contraseña debe incluir al menos una letra mayúscula.")
        return True
    
    @staticmethod
    def validar_cliente(client: Client)-> bool:
        validator.validar_email(client.email)
        validator.validar_email_duplicado(client.email)
        validator.validar_password(client.password)
        return True