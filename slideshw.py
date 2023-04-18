import tkinter as tk
from itertools import cycle
from PIL import ImageTk, Image
from time import gmtime, strftime
import glob, os, json, logging, time, signal, requests

# Configuracion del json
with open('config.json','r') as file: 
  config = json.load(file)
  cmd_actualizar = 'git pull ' + config['GIT']['URL']
  var_apagar = int(config['TIME']['APAGAR'])
  var_encender = int(config['TIME']['ENCENDER'])
  var_urlphp = config['LOCAL']['URL']
  var_config = int(config['CONFIGURATION']['OPTION']) 
  var_update = int(config['TIME']['UPDATE'])

# Variables globals de configuracion
cmd_chdir = ("cd " + os.getcwd())
cmd_reiniciar = "python3 slideshw.py"
apagar_display = "vcgencmd display_power 0"
encender_display = "vcgencmd display_power 1"
var_apiImg = requests.get('https://xelapan.com/carrusel/ws-imagenes.php')
mydata = json.loads(var_apiImg.content)

# Elimina las imagenes de la pantalla de publicidad
def delete_img():
    try:
        removing_png = glob.glob(os.getcwd() + '/*.png')
        removing_jpg = glob.glob(os.getcwd() + '/*.jpg')

        for i in removing_png:
            os.remove(i)
        for i in removing_jpg:
            os.remove(i)
        print('Eliminando las imagenes')
    except Exception as ex:
        logging.exception(str(ex)) 


# Descargar imagenes para la pantalla de publicidad
def download_img():
    try:
        for data in mydata['img']:
            with open(data['name'], 'wb') as img:
                img.write(requests.get(var_urlphp + data['name']).content)
            print('Descargando: ' + data['name'])
    except Exception as ex:
        logging.exception(str(ex)) 

def verificarHorario():
    try:
        now = int(strftime("%H"))
        #Verifica actualizar imagenes entre las 22hrs y 5am
        if now >= var_apagar and now <= var_encender:
            os.system(cmd_chdir)
            if var_config == 0:
                os.system(cmd_chdir + '/publicidad && ' + cmd_actualizar)
            elif var_config == 1:
                delete_img()
                download_img()
            quit()
        elif now == var_update:
            os.system(cmd_chdir + '/publicidad && ' + cmd_actualizar)
            print('Actualizar')
    except Exception as ex:
        logging.exception(str(ex)) 

def slideShow():
    try:
        verificarHorario()
        img = next(photos)
        displayCanvas.config(image=img)
        ####
        #### Aqui se actualiza el tiempo
        ####
        root.after(5000, slideShow) # xx seconds
        ###print("Sliding!! " + str(n))
    except Exception as ex:
        logging.exception(str(ex)) 

try: 
    logging.basicConfig(filename='error.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    logging.info('Se inicio el programa')  
    #### MAIN o
    os.system(encender_display)
    os.system(cmd_chdir)
    if var_config == 0:
        os.system(cmd_chdir + '/publicidad && '+ cmd_actualizar)
    elif var_config == 1:
        download_img()
    else:
        print('No esta permitido la configuracion ' + str(var_config))
        quit()
    
    root = tk.Tk()
    root.overrideredirect(True)
    root.config(cursor="none")  # hide the mouse cursor
    width = root.winfo_screenwidth()
    height = root.winfo_screenwidth()

    Album = []
    for image in glob.glob("./publicidad/*.jpg"):
        img = Image.open(image)
        ratio = min(width/img.width, height/img.height)
        img = img.resize((int(img.width*ratio), int(img.height*ratio)))
        Album.append(ImageTk.PhotoImage(img))
    photos = cycle(Album)

    root.geometry('%dx%d' % (width, height))
    displayCanvas = tk.Label(root)
    displayCanvas.pack()
    signal.signal(signal.SIGINT, lambda x, y: root.destroy())
    root.after(1, lambda: slideShow())
    root.bind_all('<Control-c>', lambda e: root.destroy())
    root.mainloop()
    logging.info('Se cerro el programa')
except Exception as ex:
    logging.exception(str(ex)) 
