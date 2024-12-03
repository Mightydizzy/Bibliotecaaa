import requests

API_URL = "https://poo.nsideas.cl/api/libros"

def obtener_libros():
    try:
        response = requests.get(API_URL, timeout=10)

        if response.status_code == 200:
            libros = response.json()
            print("Libros obtenidos de la API:")
            for libro in libros:
                print(f"Título: {libro['titulo']}")
                print(f"Autor: {libro['autor']}")
                print(f"Descripción: {libro['descripcion']}")
                print(f"ISBN: {libro['isbn']}")
                print(f"Número de páginas: {libro['numero_paginas']}")
                print(f"Categorías: {', '.join(libro['categorias'])}")
                print("-" * 40)
        else:
            print(f"Error al obtener libros. Código de estado: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error en la solicitud a la API: {e}")

if __name__ == "__main__":
    obtener_libros()