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

# Descargar imagenes para la pantalla de publicidad
def download_img():
    try:
        for key, value in var_urlphp.items():
            folder_path = os.getcwd() + '/publicidad'
            if var_urlphp.get(key) and var_api.get(key):
                var_apiImg = requests.get(var_api.get(key))
                mydata = json.loads(var_apiImg.content)
                for data in mydata['img']:
                    file_path = os.path.join(folder_path, data['name'])
                    with open(file_path, 'wb') as img:
                        img.write(requests.get(var_urlphp.get(key) + data['name']).content)
                    print('Descargando: ' + data['name'])
    except Exception as ex:
        logging.exception(str(ex))

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
    if var_config == 0:
        os.system(cmd_chdir + '/publicidad && '+ cmd_actualizar)
    elif var_config == 1:
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