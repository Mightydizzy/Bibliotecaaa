import requests
from src.services.api_config import API_BASE_URL

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
            raise ValueError(f"Error al conectar con la API: {e}")
