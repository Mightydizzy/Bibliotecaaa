import pymysql
import atexit
connection = None

def conectar_db():
    global connection
    if connection is None:
        try:
            connection = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',       
                password='',        
                database='biblioteca'
            )
            print("Conexión establecida a la base de datos 'biblioteca'.")
        except pymysql.MySQLError as e:
            print(f"Error al conectar a la base de datos: {e}")
            connection = None
    return connection

conectar_db()

#se ha comentado esta parte del código ya que las tablas ya se encuentran creadas, pero se conservan en caso de que haya algún error
"""
def crear_tablas():
    conn = conectar_db()  
    try:
        with conn.cursor() as cursor:
            cursor.execute(""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            );
            "")
            print("Tabla 'usuarios' verificada o creada.")

            cursor.execute(""
            CREATE TABLE IF NOT EXISTS libros (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(100) NOT NULL,
                autor VARCHAR(100),
                isbn VARCHAR(20) UNIQUE,
                disponibilidad BOOLEAN DEFAULT TRUE
            );
            "")
            print("Tabla 'libros' verificada o creada.")

            cursor.execute(""
            CREATE TABLE IF NOT EXISTS prestamos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                libro_id INT NOT NULL,
                fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_devolucion TIMESTAMP NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY (libro_id) REFERENCES libros(id)
            );
            "")
            print("Tabla 'prestamos' verificada o creada.")
        conn.commit()
    except pymysql.MySQLError as e:
        print(f"Error al crear tablas: {e}")
        """

