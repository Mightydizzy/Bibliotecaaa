import requests
from src.utils.api_config import API_BASE_URL
from src.services.error_log import ErrorLogger 

class APIClient:
    """Clase para manejar la interacción con la API."""

    def __init__(self):
        
        self.base_url = API_BASE_URL

    def get(self, endpoint: str):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            ErrorLogger.log_error(str(e), module="Api client")
            raise ValueError(f"Error al conectar con la API: {e}")
