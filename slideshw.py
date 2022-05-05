import tkinter as tk
from itertools import cycle
from PIL import ImageTk, Image
import time
from time import gmtime, strftime
import glob, os

cmd_chdir = ("cd " + os.getcwd())
cmd_actualizar = "git pull https://github.com/wichogg/publi"
cmd_reiniciar = "python slideshw.py"
cmd_kill = "pkill slideshw.py"

def verificarHorario():
  now = int(strftime("%H"))
  if now >= 22 and now <= 6:
    apagar = "echo 123 | sudo -S rtcwake -m mem --date " + strftime("%Y%m%d060100")
    os.system(cmd_kill)
    os.system(apagar)
    os.system(cmd_reiniciar)

def slideShow():
  img = next(photos)
  displayCanvas.config(image=img)
  root.after(10000, slideShow) # xx seconds
  ###print("Sliding!! " + str(n))

#### MAIN
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
root.after(5, lambda: slideShow())
root.mainloop()
