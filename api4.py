import requests

print("Bienvenido a tu biblioteca")
print("Lista de libros :3")
libros = requests.get("https://poo.nsideas.cl/api/libros")

for libro in libros.json():
        print(f"Título: {libro["titulo"]}, Autor: {libro["autor"]}, ISBN {libro["isbn"]}")

isbn = input("Ingrese el isbn del libro: ")
libros = requests.get(f"https://poo.nsideas.cl/api/libros{isbn}")

if isbn == isbn:
        print(f"autor: {libro["autor"]}")
        print(f"titulo: {libro["titulo"]}")
        print(f"categoria: {libro["categorias"]}")
        print(f"paginas: {libro["numero_paginas"]}")
        print(f"descripcion: {libro["descripcion"]}")