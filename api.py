import requests

API_URL = "https://poo.nsideas.cl/api/libros"

def obtener_libros():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los libros. Código de estado: {response.status_code}")
        return []

def filtrar_libros_por_autor(libros, autor):
    return [libro for libro in libros if libro["autor"].lower() == autor.lower()]

def main():
    print("Filtrar libros por autor")
    autor_input = input("Ingresa el nombre del autor: ").strip()

    libros = obtener_libros()

    if not libros:
        print("No se encontraron libros en la API.")
        return

    libros_filtrados = filtrar_libros_por_autor(libros, autor_input)

    if libros_filtrados:
        print(f"\nLibros encontrados del autor '{autor_input}':")
        for libro in libros_filtrados:
            print(f"Título: {libro['titulo']}")
            print(f"Descripción: {libro['descripcion']}")
            print(f"ISBN: {libro['isbn']}")
            print(f"Número de páginas: {libro['numero_paginas']}")
            print(f"Categorías: {', '.join(libro['categorias'])}")
            print("-" * 40)
    else:
        print(f"No se encontraron libros del autor '{autor_input}'.")

if __name__ == "__main__":
    main()
