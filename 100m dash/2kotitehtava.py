import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import random
import time as t
from playsound import playsound
import threading

ernesti_koordinaatti = 10
kernesti_koordinaatti = 10
kisa_ohi = False
treenin_kerroin=100

#asetetaan matka
RACE_DISTANCE = 100
UI_DISTANCE = 700

#äänet
sound1 = "stepsgrasscut.wav"
sound2 = "stepssnowcut.wav"

#Tuodaan 100m tulokset
filename = '100m.csv'

#Luetaan tiedot
data = pd.read_csv(filename, sep=';')

#Tulostetaan tiedot
#print(data)

#Luodaan uusi dictionary
wctimes ={}

#Käydään tiedot läpi ja tallennetaan ne dictionaryyn
for i in range(len(data)):
    athlete = data['Athlete'][i]
    time = data['Time'][i]
    if athlete not in wctimes:
        wctimes[athlete] = []
    wctimes[athlete].append(time)

#Tulostetaan dictionary
#print(wctimes)
    
#Lisätään leijonat dictionaryyn
wctimes['LeoLeijona'] = [8,00]
wctimes['LeaLeijona'] = [8,10]
wctimes['LasseLeijona'] = [8,20]
wctimes['LenniLeijona'] = [8,30]
wctimes['LauriLeijona'] = [8,40]
wctimes['LindaLeijona'] = [8,50]
wctimes['LottaLeijona'] = [9,00]
wctimes['LumiLeijona'] = [9,10]
wctimes['LunaLeijona'] = [9,20]
wctimes['LaiskaLeijona'] = [19,30]

#Alustetaaan tkinter
ikkuna = tk.Tk()
ikkuna.title("Juoksutreenit")
ikkuna.geometry("800x600+100+100")


#Funktio, joka suoritetaan kun painiketta painetaan
def aani():
    playsound(sound1)

def aani2():
    playsound(sound2)

def nayta_tulokset_popup(tulokset):
    popup = tk.Toplevel()
    popup.title("100m tulokset")
    popup.geometry("300x200")

    for juoksija, time in tulokset.items():
        label = tk.Label(popup, text=f"{juoksija}: {time}")
        label.pack(pady=10)

    close_button = tk.Button(popup, text="Sulje", command=popup.destroy)
    close_button.pack(pady=20)

def yhteislahto():
    global kisa_ohi, treenin_kerroin
    duration1 = random.uniform(12, 20)*(treenin_kerroin/100)
    duration2 = random.uniform(12, 20)*(treenin_kerroin/100)
    
    thread1 = threading.Thread(target=lahetaErnsesti, args=(duration1,))
    thread2 = threading.Thread(target=lahetaKernesti, args=(duration2,))
    
    thread1.start()
    thread2.start()


def lahetaErnsesti(duration=None):
    global ernesti_koordinaatti, treenin_kerroin
    print("Lähetetään ernesti juoksemaan")
    aani_thread1 = threading.Thread(target=aani)
    aani_thread1.start()

    if duration is None:
        duration = random.uniform(12, 20)*(treenin_kerroin/100)
    liikuta_henkiloa(duration, ernestiMerkki, ernesti_koordinaatti)
    
    ernesti_koordinaatti = ernestiMerkki.winfo_x()
    wctimes['Ernesti'] = [duration]
    print(f"Ernesti juoksi 100m {duration} sekuntia")

    aani_thread1.join()
    tarkasta_tilanne()
    return duration


def lahetaKernesti(duration=None):
    global kernesti_koordinaatti, treenin_kerroin
    print("Lähetetään kernesti juoksemaan")
    #luodaan äänithreadi
    aani_thread1 = threading.Thread(target=aani2)
    aani_thread1.start()
   
    #arvotaan aika
    if duration is None:
        duration = random.uniform(12, 20)*(treenin_kerroin/100)
    liikuta_henkiloa(duration, kernestiMerkki, kernesti_koordinaatti)

    #loppuaika
    kernesti_koordinaatti = kernestiMerkki.winfo_x()
    wctimes['Kernesti'] = [duration]
    print(f"Kernesti juoksi 100m {duration} sekuntia")

    aani_thread1.join()
    tarkasta_tilanne()
    return duration

def liikuta_henkiloa(duration, merkki, merkkikoordinaatti):
    print("duration henkilön liikutuksessa", duration , merkkikoordinaatti)
    askeleet= 100
    viive = duration / askeleet
    matka_per_askel = UI_DISTANCE / askeleet

    for askel in range(askeleet):
        print(f"Step {askel+1}/{askeleet}")
        merkkikoordinaatti += matka_per_askel
        merkki.place(x=merkkikoordinaatti)
        print("liikutus onnistuu")
        ikkuna.update()
        t.sleep(viive)

def tarkasta_tilanne():
    global kisa_ohi
    if ernesti_koordinaatti >= UI_DISTANCE and kernesti_koordinaatti >= UI_DISTANCE:
        print("Kisa on ohi")
        kisa_ohi = True
        tulokset = {'Ernesti': wctimes['Ernesti'], 'Kernesti': wctimes['Kernesti']}
        nayta_tulokset_popup(tulokset)

def treenit():
    global treenin_kerroin
    treenin_kerroin-=1
    print("Treenin kerroin", treenin_kerroin)


#Lisätään merkit
ernestiMerkki = tk.Label(ikkuna, text='E')
ernestiMerkki.place(x=10, y=380)

kernestiMerkki = tk.Label(ikkuna, text='K')
kernestiMerkki.place(x=10, y=400)

#lisätään nappi
painike = tk.Button(ikkuna, text="Ernestin lähtö", command=lahetaErnsesti)
painike.place(x=10, y=10)

painike2 = tk.Button(ikkuna, text="Kernestin lähtö", command=lahetaKernesti)
painike2.place(x=10, y=50)

painike3 = tk.Button(ikkuna, text='Yhteislähtö', command=yhteislahto)
painike3.place(x=10, y=90)

painike4= tk.Button(ikkuna, text='Treenit', command=treenit)
painike4.place(x=500, y=10)

ikkuna.mainloop()


