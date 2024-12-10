from datetime import datetime
from src.models.connection import Connection

class ErrorLogger:

    @staticmethod
    def log_error(message: str, module: str, trace: str = None):
        query = " INSERT INTO logs (error_message, module, error_trace, timestamp) VALUES (%s, %s, %s, %s)"
    
        try:
            with Connection() as db:
                # Insertar el log del error en la base de datos
                db.execute_query(query, (message, module, trace, datetime.now()))
        except Exception as e:
            print(f"Error crítico al registrar en logs: {e}")

