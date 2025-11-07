from datetime import datetime, timedelta
import glob
import json
import logging
import os
from time import strftime
import time
import cv2
import requests
from screeninfo import get_monitors
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pathlib import Path
import threading

session = requests.Session()
retry = Retry(
    total=3,  
    backoff_factor=2.0,  
    status_forcelist=[500, 502, 503, 504]  
)
adapter = HTTPAdapter(max_retries=retry)
# Montar el adaptador para todas las URLs
session.mount('http://', adapter)
session.mount('https://', adapter)
with open('config.json','r') as file: 
    config = json.load(file)
    cmd_actualizar = 'git pull ' + config['GIT']['URL']
    var_urlphp = config.get('LOCAL')
    var_api = config.get('API')
    var_config = int(config['CONFIGURATION']['OPTION']) 
    var_horaUpdate = int(config['UPDATE']['HOUR'])
    var_minutoUpdate = int(config['UPDATE']['MINUTE'])
    var_diaUpdate = config['UPDATE']['DAY']

def actualizar_repositorio():
    try:
        os.system('git pull origin test')
        logging.info('Repositorio actualizado correctamente')
    except Exception as ex:
        logging.exception('Error al actualizar el repositorio: ' + str(ex))
# Variables globals de configuracion
cmd_chdir = ("cd " + os.getcwd())
cmd_reiniciar = "python3 slideshw.py"
monitor = get_monitors()[0]
width, height = monitor.width, monitor.height
last_connectivity_check = 0
connectivity_check_interval = 300  # 5 minutos
is_connected = True
should_update = False
last_update_day = None

def verificarInternet():
    global last_connectivity_check, connectivity_check_interval, is_connected
    current_time = time.time()
    # Solo verificar conectividad cada 5 minutos
    if current_time - last_connectivity_check < connectivity_check_interval:
        return is_connected
    try:
        # Usar HEAD request en lugar de GET para reducir tráfico
        response = session.head('https://www.google.com', timeout=3)
        is_connected = response.status_code == 200
        last_connectivity_check = current_time
        return is_connected
    except:
        is_connected = False
        last_connectivity_check = current_time
        return False
    
def get_images_from_api(api_url):
    try:
        response = session.get(api_url, timeout=5)
        response.raise_for_status()
        return [item['name'] for item in response.json().get('img', [])]
    except Exception as ex:
        logging.exception(f"Error obteniendo imágenes desde {api_url}: {ex}")
        return []

def download_image(image_url, file_path, retries=3):
    for attempt in range(1, retries + 1):
        try:
            response = session.get(image_url, timeout=3)
            response.raise_for_status()
            file_path.write_bytes(response.content)
            print(f"✅ Descargado: {file_path.name}")
            return True
        except Exception as ex:
            print(f"❌ Error {attempt}/{retries} al descargar {image_url}: {ex}")
            if attempt == retries:
                logging.exception(f"Fallo definitivo descargando {image_url}: {ex}")
            else:
                time.sleep(attempt * 2)  # backoff exponencial
    return False

def verificarArchivos(var_urlphp, var_api):
    folder_path = Path.cwd() / "publicidad"
    todos = set()
    for key, base_url in var_urlphp.items():
        api_url = var_api.get(key)
        if not (api_url and base_url):
            continue
        # 1. Nombres esperados desde la API
        nombres_api = set(get_images_from_api(api_url))
        if nombres_api:
            todos.update(nombres_api)
    # 2. Nombres de archivos que ya existen en la carpeta
    existentes = {f.name for f in folder_path.iterdir() if f.is_file()}
    if todos == existentes:
        print(f"✔ Todas las imágenes ya están sincronizadas.")
        return True
    else:
        print("⚠ Es necesario actualizar la carpeta.")
        return False
def descargar_todas(var_urlphp, var_api):
    folder_path = Path.cwd() / "publicidad"
    folder_path.mkdir(exist_ok=True)  # crea carpeta si no existe
    exitos, fallos = [], []
    todos = set()
    api_data = {}
    for key, base_url in var_urlphp.items():
        api_url = var_api.get(key)
        if not (api_url and base_url):
            continue
        nombres_api = set(get_images_from_api(api_url))
        if nombres_api:
            todos.update(nombres_api)
            api_data[key] = {
                "base_url": base_url,
                "nombres": nombres_api
            }
    existentes = {f.name for f in folder_path.iterdir() if f.is_file()}
    # 3. Eliminar archivos sobrantes
    sobrantes = existentes - todos
    for archivo in sobrantes:
        try:
            (folder_path / archivo).unlink()
            print(f"🗑 Eliminado archivo sobrante: {archivo}")
        except Exception as ex:
            logging.exception(f"No se pudo eliminar {archivo}: {ex}")

    for key, data in api_data.items():
        base_url = data["base_url"]
        nombres_api = data["nombres"]
        faltantes = nombres_api - {f.name for f in folder_path.iterdir() if f.is_file()}
        if not faltantes:
            print(f"✔ Todas las imágenes de {key} ya están sincronizadas.")
            continue
        print(f"🔍 En {key}: {len(faltantes)} archivos faltan, iniciando descarga...")
        for name in faltantes:
            image_url = f"{base_url}{name}"
            file_path = folder_path / name
            if download_image(image_url, file_path):
                exitos.append(name)
            else:
                fallos.append(name)

    print(f"\n📊 Descargas completadas: {len(exitos)} exitosas, {len(fallos)} fallidas")

def show_media(file_path):
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


def runPresentacion():
    global should_update
    try:
        os.makedirs('publicidad', exist_ok=True)    
        if verificarArchivos(var_urlphp, var_api):
            print("No se requieren descargas.")
        else:
            descargar_todas(var_urlphp, var_api)
        cv2.destroyAllWindows()
        cv2.namedWindow("Presentación", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Presentación", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while True:
            # Procesar cada archivo media
            media_files = glob.glob('publicidad/*.*')
            for media_file in media_files:
                if should_update:
                    print("⏹ Iniciando actualización (no detendrá la presentación si falla)...")
                    try:
                        if verificarInternet():
                            if verificarArchivos(var_urlphp, var_api):
                                print("✔ No se requieren descargas.")
                            else:
                                descargar_todas(var_urlphp, var_api)
                        else:
                            print("⚠️ No hay internet, reintentará más tarde.")
                    except Exception as e:
                        print(f"⚠️ Error durante actualización: {e}")
                    finally:
                        should_update = False
                        # Refrescar la lista de medios sin salir del ciclo
                        media_files = glob.glob('publicidad/*.*')
                        cv2.destroyAllWindows()
                        cv2.namedWindow("Presentación", cv2.WND_PROP_FULLSCREEN)
                        cv2.setWindowProperty("Presentación", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                # Mostrar imágenes
                if media_file.endswith((".jpg", ".png", ".jpeg")):
                    image = cv2.imread(media_file)
                    if image is not None:
                        image = cv2.resize(image, (width, height))
                        for _ in range(50):  # 5 segundos con chequeos cada 0.1s
                            cv2.imshow("Presentación", image)
                            if should_update or cv2.waitKey(100) & 0xFF == 27:
                                break
                        if should_update:
                            break
                elif media_file.endswith((".mp4", ".avi", ".gif")):
                    show_media(media_file)
                # Verificar si el usuario quiere salir
                if cv2.waitKey(1) & 0xFF == 27:  # Salir con la tecla Esc
                    break
    except Exception as e:
        print(f"Ocurrio un error: {e}")

def monitor_update_time():
    global should_update, last_update_day
    while True:
        now = datetime.now()
        scheduled_time = datetime.strptime(f"{var_horaUpdate}:{var_minutoUpdate}", "%H:%M").time()
        scheduled_dt = datetime.combine(now.date(), scheduled_time)
        window_end = scheduled_dt + timedelta(minutes=5)
        # Si está dentro del rango y no se actualizó hoy
        if scheduled_dt <= now <= window_end and last_update_day != now.date():
            print("🕒 Hora de actualización detectada.")
            should_update = True
            last_update_day = now.date()
        time.sleep(10)
if __name__ == "__main__":
    try:
        logging.basicConfig(filename='error.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.info('Se inicio el programa') 
        actualizar_repositorio()
        #Hilo para la actualizacion 
        threading.Thread(target=monitor_update_time, daemon=True).start()
        # proyecto
        runPresentacion()
    except Exception as e:
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.exception(f"[{fecha}] Error ocurrió un error: {e}")
