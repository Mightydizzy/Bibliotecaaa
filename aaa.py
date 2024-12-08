class Libro:
    
    def __init__(self, isbn: str, titulo: str, autor: str, descripcion: str, categorias: str, numero_paginas: int, disponibilidad: bool):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.descripcion = descripcion
        self.categorias = categorias
        self.numero_paginas = numero_paginas
        self.disponibilidad = disponibilidad

    def __repr__(self):
        return f"Libro({self.isbn}, {self.titulo}, {self.autor}, {self.numero_paginas} páginas, Disponible: {self.disponibilidad})"

    def marcar_disponible(self):
        self.disponibilidad = True

    def marcar_no_disponible(self):
        self.disponibilidad = False

    def from_dict(cls, data: dict):
        return cls(
            isbn=data.get("isbn", ""),
            titulo=data.get("titulo", ""),
            autor=data.get("autor", ""),
            descripcion=data.get("descripcion", ""),
            categorias=", ".join(data.get("categorias", [])),  # Convierte lista de categorías a cadena
            numero_paginas=data.get("numero_paginas", 0),
            disponibilidad=data.get("disponibilidad", True),
        )
