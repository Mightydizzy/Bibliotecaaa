class Client:
    def __init__(self, id_cliente=None, nombre= None, email=None, password=None):
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__email = email
        self.__password = password

    @property
    def id_cliente(self):
        return self.__id_cliente
        
    # Getter para nombre
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre


    # Getter para email
    @property
    def email(self):
        return self.__email

    def get_password(self):
        return self.__password
