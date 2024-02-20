import glob
import json
import logging
import os
from time import strftime
import cv2
import requests
from screeninfo import get_monitors

with open('config.json','r') as file: 
    config = json.load(file)
    
    #cmd_actualizar = 'git pull ' + config['GIT']['URL']
    var_apagar = int(config['TIME']['APAGAR'])
    var_encender = int(config['TIME']['ENCENDER'])
    var_urlphp = config.get('LOCAL')
    var_api = config.get('API')
    var_config = int(config['CONFIGURATION']['OPTION']) 
    var_update = int(config['TIME']['UPDATE'])

# Variables globals de configuracion
cmd_chdir = ("cd " + os.getcwd())
cmd_reiniciar = "python3 slideshw.py"
apagar_display = "vcgencmd display_power 0"
encender_display = "vcgencmd display_power 1"
#var_apiImg = requests.get('https://xelapan.com/carrusel/ws-imagenes.php')
#mydata = json.loads(var_apiImg.content)

#Eliminar las imagenes de la pantalla de publicidad
def delete_img():
    try:
        #time.sleep(10)
        if requests.get('https://www.google.com', timeout=5).status_code == 200:
            removing_extensions = ['png', 'jpg', 'mp4', 'gif','jpeg']
            for ext in removing_extensions:
                file_list = glob.glob(os.getcwd() + f'/publicidad/*.{ext}')
                for file in file_list:
                    os.remove(file)
            print('Eliminando los archivos')
        else:
            print('No se pudo conectar a internet para eliminar los archivos.')
    except requests.ConnectionError as e:
        print(f"Error de conexión: {str(e)}")
    except Exception as ex:
        logging.exception(str(ex))
def descargar():
    try:
        with requests.Session() as s:  # Usar una sesión para reutilizar la conexión TCP
            for key, value in var_urlphp.items():
                folder_path = os.getcwd() + '/publicidad'
                if var_urlphp.get(key) and var_api.get(key):
                    var_apiImg = s.get(var_api.get(key), timeout=5)  # Añadir un tiempo de espera
                    mydata = json.loads(var_apiImg.content)
                    for data in mydata['img']:
                        file_path = os.path.join(folder_path, data['name'])
                        image_url = var_urlphp.get(key) + data['name']
                        for i in range(3):  # Intentar descargar la imagen hasta 3 veces
                            try:
                                response = s.get(image_url, timeout=2)  # Añadir un tiempo de espera
                                with open(file_path, 'wb') as img:
                                    img.write(response.content)
                                print('Descargado: ' + data['name'])
                                break  # Si la descarga fue exitosa, salir del bucle
                            except Exception as ex:
                                print('Error descargando imagen: ' + image_url + '. Intento: ' + str(i+1))
                                if i == 2:  # Si este fue el último intento, registrar el error
                                    logging.exception('Error descargando imagen: ' + image_url + '. Error: ' + str(ex))
    except Exception as ex:
        logging.exception('Error general: ' + str(ex))
def download_img():
    try:
        nombres = []  # Lista para guardar los nombres
        for key, url in var_api.items():
            if url:  # Verifica que la URL no esté vacía
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()  # Suponiendo que las APIs devuelven JSON
                    for item in data['img']:
                        nombres.append(item['name'])  # Agrega el nombre a la lista
                else:
                    print(f"Error al obtener datos de {key}: {response.status_code}")
        folder_path = os.getcwd() + '/publicidad'       
        while True:
            files = os.listdir(folder_path)
            if len(files) == len(nombres):
                print("descarga completa")
                break
            else:
                delete_img()
                descargar()
    except Exception as ex:
        logging.exception('Error descargando imágenes: ' + str(ex))
def verificarHorario():
    try:
        now = int(strftime("%H"))
        #Verifica actualizar imagenes entre las 22hrs y 5am
        if now >= var_apagar and now <= var_encender:
            if var_config == 1:
                delete_img()
                download_img()
            quit()
        elif now == var_update:
            delete_img()
            download_img()
    except Exception as ex:
        logging.exception(str(ex)) 
# Función para mostrar medios (imagen o video) en pantalla completa
def show_media(file_path):
    verificarHorario()
    cap = cv2.VideoCapture(file_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (width, height))
        cv2.imshow("Presentación", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Salir con la tecla Esc
            break
    cap.release()
try:
    logging.basicConfig(filename='error.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info('Se inicio el programa')  
    #### MAIN o
    os.system(encender_display)
    os.system(cmd_chdir)
    if var_config == 1:
        delete_img()
        download_img()
    else:
        print('No esta permitido la configuracion ' + str(var_config))
        quit()
    # Obtiene el nombre de los archivos multimedia de publicidad  
    media_folder = "publicidad"
    media_files = []
    for filename in os.listdir(media_folder):
        media_files.append(os.path.join(media_folder, filename))

    # Obtiene el tamaño del monitor principal
    monitor = get_monitors()[0]
    width, height = monitor.width, monitor.height

    
    cv2.namedWindow("Presentación", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Presentación", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Recorre la lista de medios y muéstralos en pantalla completa
    while True:
        for media_file in media_files:
            if media_file.endswith((".jpg", ".png",".jpeg")):
                image = cv2.imread(media_file)
                image = cv2.resize(image, (width, height))
                cv2.imshow("Presentación", image)
                cv2.waitKey(5000)  # Esperar 5 segundos antes de pasar a la siguiente imagen
            elif media_file.endswith((".mp4", ".avi", ".gif")):
                show_media(media_file)
        if cv2.waitKey(1) & 0xFF == 27:  # Salir con la tecla Esc
            break
    # Cerrar la ventana al final
    cv2.destroyAllWindows()
except Exception as ex:
    logging.exception(str(ex))