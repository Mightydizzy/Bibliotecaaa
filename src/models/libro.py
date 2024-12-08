class Libro:

    def __init__(self, isbn, titulo, autor, descripcion, categorias, numero_paginas, disponibilidad):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.descripcion = descripcion
        self.categorias = categorias
        self.numero_paginas = numero_paginas
        self.disponibilidad = disponibilidad

    @staticmethod
    def from_dict(data):
        return Libro(
            isbn=data.get("isbn"),
            titulo=data.get("titulo"),
            autor=data.get("autor"),
            descripcion=data.get("descripcion"),
            categorias=",".join(data.get("categorias", [])),  # Convierte lista a string
            numero_paginas=data.get("numero_paginas"),
            disponibilidad=True  # Por defecto, disponible al deserializar
        )
    def to_dict(self):
        """Convierte la instancia a un diccionario."""
        return {
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "descripcion": self.descripcion,
            "categorias": self.categorias,
            "numero_paginas": self.numero_paginas,
            "disponibilidad": self.disponibilidad,
        }
