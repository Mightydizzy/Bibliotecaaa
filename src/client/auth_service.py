from src.models.connection import Connection
from src.utils.hashing import verify_pw
from src.models.class_client import Client

class AuthService:
    def authenticate_client(self, email: str, password: str) -> dict:
        try:
            with Connection() as connection:
                cursor = connection.execute_query("""
                    SELECT id, nombre, email, password_hash
                    FROM usuarios
                    WHERE email = %s
                """, (email,))
                
                resultado = cursor.fetchone()
                if resultado:
                    id_cliente, nombre, email, password_hash = resultado
                    if verify_pw(password, password_hash):
                        print("Autenticación exitosa.")
                        return Client(id_cliente=id_cliente, nombre=nombre, email=email)
                    else:
                        print("Contraseña incorrecta.")
                else:
                    print("Cliente no encontrado.")
        except Exception as e:
            print(f"Error al autenticar cliente: {e}")
        
        return None