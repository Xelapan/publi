import tkinter as tk
from itertools import cycle
from PIL import ImageTk, Image
import time
from time import gmtime, strftime
import os
import git 

def GetAlbum():
  return ["Slide1.png", 
            "Slide2.png", 
            "Slide3.png",
            "Slide4.png"]


def verificarHorario():
  now = int(strftime("%H"))
  if now >= 22 and now <= 6:
      apagar = "echo 123 | sudo -S rtcwake -m mem --date " + strftime("%Y%m%d060100")
      os.system(apagar)
  

def slideShow():
  global n
  img = next(photos)
  displayCanvas.config(image=img)
  root.after(2000, slideShow) # xx seconds
  n = n + 1
  print("Sliding!! " + str(n))
  if n > 3:
    root.destroy()

def updatefiles():
  print("")

root = tk.Tk()
root.overrideredirect(True)
root.config(cursor="none")  # hide the mouse cursor
width = root.winfo_screenwidth()
height = root.winfo_screenwidth()
n = 0

images = GetAlbum()
Album = []
for image in images:
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
root.after(10, lambda: slideShow())
root.mainloop()
print("holaaa ")