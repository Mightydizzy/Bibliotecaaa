from src.db_connection import conectar_db
from src.utils.hashing import verify_pw

def autenticar_cliente(email, password):
    connection = conectar_db
    if not connection:
        print("No se pudo conectar a la base de datos.")
        return
    try: 
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT id, nombre, email, password_hash FROM usuarios WHERE email = %s
            """, (email,))
            resultado = cursor.fetchone()
            if resultado:
                id_cliente, nombre, email, password_hash = resultado
                if verify_pw(password, password_hash):
                    print("Autenticación exitosa.")
                    return {
                        "id": id_cliente,
                        "nombre" : nombre,
                        "email" : email
                    }
                else: print("Contraseña incorrecta.")
            else:
                print("Cliente no encontrado.")
    except Exception as e:
        print("Error al autenticar cliente: {e}")
    finally: 
        connection.close()
    return None
