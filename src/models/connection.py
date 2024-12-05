import pymysql

class Connection:
    def __init__(self, host='localhost', port=3306, user='root', password='', database='Biblioteca'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except pymysql.MySQLError as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.connection = None

    def close(self):
        if self.connection and self.connection.open:
            self.connection.close()
    def execute_query(self, query, params=None):
        if not self.connection or not self.connection.open:
            raise ConnectionError("No hay una conexión activa a la base de datos.")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return cursor
        except pymysql.MySQLError as e:
            print(f"Error al ejecutar la consulta: {e}")
            raise

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
