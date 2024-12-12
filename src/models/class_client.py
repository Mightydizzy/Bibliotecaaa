class Client:
    def __init__(self, id_cliente=None, nombre= None, email=None, password=None):
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__email = email
        self.__password = password

    def id_cliente(self):
        return self.__id_cliente
        
    def nombre(self):
        return self.__nombre
    
    def nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

    def email(self):
        return self.__email

    def get_password(self):
        return self.__password
