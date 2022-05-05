import tkinter as tk
from itertools import cycle
from PIL import ImageTk, Image
import time
from time import gmtime, strftime
import glob, os

cmd_chdir = ("cd " + os.getcwd())
cmd_actualizar = "git pull https://github.com/wichogg/publi"
cmd_reiniciar = "python slideshw.py"
apagar_display = "vcgencmd display_power 0"
encender_display = "vcgencmd display_power 1"

def verificarHorario():
  now = int(strftime("%H"))
  #Verifica apagarse entre 10pm y 5AM
  if now >= 15 and now <= 16:
    #apagar display
    os.system(apagar_display)
    if now <= 10:
      tsleep = (23 - now) + 5
    else: 
      tsleep = 16 - now
    #Dormir el programa
    time.sleep((tsleep * 3600) + 2)
    os.system(encender_display)
    os.system(cmd_reiniciar)
    quit()

def slideShow():
  img = next(photos)
  displayCanvas.config(image=img)
  ####
  #### Aqui se actualiza el tiempo
  ####
  root.after(5000, slideShow) # xx seconds
  verificarHorario()
  ###print("Sliding!! " + str(n))

#### MAIN o
os.system(encender_display)
os.system(cmd_chdir)
os.system(cmd_actualizar)
root = tk.Tk()
root.overrideredirect(True)
root.config(cursor="none")  # hide the mouse cursor
width = root.winfo_screenwidth()
height = root.winfo_screenwidth()

Album = []
for image in glob.glob("*.jpg"):
    img = Image.open(image)
   # if img.width > width or img.height > height:
        # only resize image bigger than the screen
    ratio = min(width/img.width, height/img.height)
    img = img.resize((int(img.width*ratio), int(img.height*ratio)))
    Album.append(ImageTk.PhotoImage(img))
photos = cycle(Album)

root.geometry('%dx%d' % (width, height))
displayCanvas = tk.Label(root)
displayCanvas.pack()
#stime.sleep(10)
root.after(1, lambda: slideShow())
root.mainloop()
