import requests

print("Bienvenido a la API de libros")
print("Lista de libros")
response_libros = requests.get("https://poo.nsideas.cl/api/libros")

if response_libros.status_code == 200:
    for libro in response_libros.json():
        print(f"Título: {libro["titulo"]}, Autor: {libro["autor"]}, ISBN: {libro["isbn"]}")

