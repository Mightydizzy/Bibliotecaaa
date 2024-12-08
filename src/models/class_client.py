from src.utils.hashing import hash_password
import re
class Client:
    def __init__(self, id_cliente=None, nombre= None, email=None, password=None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.password = password
