import threading
import tkinter as tk
from PIL import Image, ImageTk
import random 

#Kuvat

#Tehdään tkinter-ikkuna
ikkuna = tk.Tk()
ikkuna.title("Tomato Throwing")
ikkuna.geometry("1300x700+100+100")


#Asetetaan maalitaulu keskelle ruutua ja sakaalataan se sopivaksi
image = Image.open("maalitaulu.png")
photo = ImageTk.PhotoImage(image)
maalitaulu = tk.Label(ikkuna, image=photo)
resized_image = image.resize((300, 350))
photo = ImageTk.PhotoImage(resized_image)
maalitaulu = tk.Label(ikkuna, image=photo)
maalitaulu.image = photo
maalitaulu.place(relx=0.5, rely=0.5, anchor="center")

#Lisätään kernest vasempaan reunaan
kernestKuva = Image.open("kerne.png")
photoK = ImageTk.PhotoImage(kernestKuva)
kernest = tk.Label(ikkuna, image=photoK)
kernest.image = photoK
kernestiY = random.uniform(0.2,0.8)
kernest.place(relx=0.005, rely=kernestiY, anchor="w")

ernestiY = random.uniform(0.2,0.8)

#lisätään ernesti funktio
def lisaa_ernest():
    global ernestiY
    ernestKuva = Image.open("erne.png")
    photoE = ImageTk.PhotoImage(ernestKuva)
    kernest = tk.Label(ikkuna, image=photoE)
    kernest.image = photoE
    kernest.place(relx=0.85, rely=ernestiY, anchor="w")

def kernesti_heitto():
    global kernestiY
    print (kernestiY)
    tomaatti=Image.open("tomaatti.png")
    photoT = ImageTk.PhotoImage(tomaatti)
    tomaatti = tk.Label(ikkuna, image=photoT)
    tomaatti.image = photoT
    tomaatti.place(relx=0.005, rely=kernestiY, anchor="w")

def liikuta_tomaatti():
    global kernestiY
    global ernestiY


        


#Napit
nappi1 = tk.Button(ikkuna, text="Lisää ernesti", command=lisaa_ernest)
nappi1.place(x=10, y=10)

nappi2 = tk.Button(ikkuna, text="Heitä kernesti", command=kernesti_heitto)
nappi2.place(x=10, y=40)

ikkuna.mainloop()