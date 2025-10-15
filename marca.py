import requests

url = "https://xelapan.com/carrusel/Publicidad/"
response = requests.get(url)

if response.status_code == 200:
    timestamp = float(response.text)
    print("Marca de tiempo del servidor:", timestamp)
else:
    print("Error al obtener la marca de tiempo del servidor:", response.status_code)
