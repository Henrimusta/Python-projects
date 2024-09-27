import tkinter as tk
import threading
import time as t
from playsound import playsound
import random

#####GLOBALS#####
#Global variables
monkey_with_message_E = 0
monkey_with_message_K = 0
ernesti_monkey_counter = 0
kernesti_monkey_counter = 0
counter_lock_E= threading.Lock()
counter_lock_K= threading.Lock()
ship_sent_E = False
ship_sent_K = False

#Sounds
splash = "splash.wav"
snap = "snap.wav"
success = "success.wav"
trumpet1 = "trumpet1.wav"
trumpet2 = "trumpet2.mp3"

#Lists for messages arrived
messages_arrived_E = []
messages_arrived_K = []

#####VISUALS#####
#Create island on the left side
def create_island(canvas):
    #Fill the window with water
    canvas.create_rectangle(0, 0, 1300, 700, fill="lightblue")

    #Draw the island
    canvas.create_rectangle(50,600,250,100, fill="lightgreen", outline="beige", width=5)

#Create mainland on the right side
def create_mainland(canvas):
    #Draw the mainland
    canvas.create_rectangle(1000, 800, 1500, 0, fill="darkgreen")
    #Draw the beach on the mainland
    canvas.create_rectangle(1050, 0, 1000, 700, fill="sandybrown", outline="sandybrown") 

#####FUNCTIONS#####
#Send monkey to swim
def monkey_swim_E():
    global monkey_with_message_E
    global ernesti_monkey_counter
    #If monkey does not have a message
    if monkey_with_message_E == 0:
        #place Ernestis monkey on the island
        monkeyMarkerE = tk.Label(window, text="Monkey")
        monkeyMarkerE.place(x=235, y=185)

        #Send monkey to swim
        for i in range(100):
            newMonkeyPosition = 235 + (i*7.7)
            monkeyMarkerE.place(x=newMonkeyPosition, y=185)
            window.update()
            print(f"Ernestis monkey location {newMonkeyPosition}, {185}")
            t.sleep(0.1)

    #If monkey has a message
    else:
        monkey_with_message = tk.Label(window, text="Monkey")
        message_to_check = monkey_with_message_E
        monkey_with_message_E = 0
        monkey_with_message.place(x=235, y=185)

        #Shark attack boolean
        shark_attacked_E = False

        #Send monkey to swim
        for i in range(100): # 1000 units = 100 km
            newMonkeyPosition = 235 + (i*7.7)

            #Check if shark attacks
            if shark_attack():
                shark_attacked_E = True
                monkey_with_message.destroy()
                break

            # Play sound every 100 units (1 km)
            if i % 10 == 0:
                threading.Thread(target=playsound, args=(splash,)).start()
                
            monkey_with_message.place(x=newMonkeyPosition, y=185)
            window.update()
            t.sleep(0.1)

        #If monkey arrives safely
        if shark_attacked_E == False:
            threading.Thread(target=playsound, args=(success,)).start()
            with counter_lock_E:
                ernesti_monkey_counter += 1
                print(f"Ernestis monkeys arrived safely: {ernesti_monkey_counter}")
                start_port_guard_watch_P(message_to_check)



def monkey_swim_K():
    global monkey_with_message_K
    global kernesti_monkey_counter
    #If monkey does not have a message
    if monkey_with_message_K == 0:
        #place Kernestis monkey on the island
        monkeyMarkerK = tk.Label(window, text="Monkey")
        monkeyMarkerK.place(x=235, y=505)

        #Send monkey to swim
        for i in range(100):
            newMonkeyPosition = 235 + (i*7.7)
            monkeyMarkerK.place(x=newMonkeyPosition, y=505)
            window.update()
            t.sleep(0.1)

    #If monkey has a message    
    else:
        monkey_with_message = tk.Label(window, text="Monkey")
        message_to_check = monkey_with_message_K
        monkey_with_message_K = 0
        monkey_with_message.place(x=235, y=505)

        #Shark attack boolean
        shark_attacked_K = False

        #Send monkey to swim
        for i in range(100):
            newMonkeyPosition = 235 + (i*7.7)

            #Check if shark attacks
            if shark_attack():
                shark_attacked_K = True
                monkey_with_message.destroy()
                break

            # Play sound every 100 units (1 km)
            if i % 10 == 0:
                threading.Thread(target=playsound, args=(splash,)).start()

            monkey_with_message.place(x=newMonkeyPosition, y=505)
            window.update()
            t.sleep(0.1)

        #If monkey arrives safely
        if shark_attacked_K == False:
            threading.Thread(target=playsound, args=(success,)).start()
            with counter_lock_K:
                kernesti_monkey_counter += 1
                print(f"Kernestis monkeys arrived safely: {kernesti_monkey_counter}")
                start_port_guard_watch_E(message_to_check)

#Teach message to monkey
def teach_message_to_swimmer_E():
    global monkey_with_message_E
    messages= ["Ernesti", "ja", "Kernesti", "tässä", "terve!", "Olemme", "autiolla", "saarella,", "voisiko", "joku", "tulla", "sieltä", "sivistyneestä", "maailmasta", "hakemaan", "meidät", "pois!", "Kiitos!"]
    monkey_with_message_E = random.choice(messages)
    print(f"Ernestis monkey has learned the message {monkey_with_message_E}")

def teach_message_to_swimmer_K():
    global monkey_with_message_K
    messages= ["Ernesti", "ja", "Kernesti", "tässä", "terve!", "Olemme", "autiolla", "saarella,", "voisiko", "joku", "tulla", "sieltä", "sivistyneestä", "maailmasta", "hakemaan", "meidät", "pois!", "Kiitos!"]
    monkey_with_message_K = random.choice(messages)
    print(f"Kernestis monkey has learned the message {monkey_with_message_K}")

#Shark attack function
def shark_attack():
    chance_to_attack = random.randint(1, 150)
    if chance_to_attack == 1:
        threading.Thread(target=playsound, args=(snap,)).start()
        print("Shark attack!")
        return True
    return False

#Send 10 monkeys to swim
def send_10_monkeys_E():
    
    def teach_10_monkeys():
        teach_message_to_swimmer_E()
        monkey_swim_E()

    def send_monkeys_with_delay():
        for i in range(10):
            threading.Thread(target=teach_10_monkeys).start()
            t.sleep(1)

    threading.Thread(target=send_monkeys_with_delay).start()

#Send 10 monkeys to swim
def send_10_monkeys_K():
    
    def teach_10_monkeys():
        teach_message_to_swimmer_K()
        monkey_swim_K()

    def send_monkeys_with_delay():
        for i in range(10):
            threading.Thread(target=teach_10_monkeys).start()
            t.sleep(1)

    threading.Thread(target=send_monkeys_with_delay).start()

#Set portguards to watch the sea for monkeys
def port_guard_watch_P(message):
    global messages_arrived_E

    #check if monkey has a message
    if message != 0:
        print ("Port guard Pohteri: Monkey with message spotted!")
        print(f"Message: {message}")

        #Check if message has already arrived
        if message not in messages_arrived_E:
            messages_arrived_E.append(message)
            print(f"Messages arrived: {messages_arrived_E}")
            if len(messages_arrived_E) == 10:
                print("Pohteri recieved 10 messages!")
                send_evacuation_ship()
        
        #If message has already arrived
        else:
            print(f"Message {message} already arrived!")

#Set portguards to watch the beach for monkeys
def port_guard_watch_E(message):
    global messages_arrived_K

    #Check if monkey has a message
    if message !=0:
        print ("Port guard Eteteri: Monkey with message spotted!")
        print(f"Message: {message}")
        
        #Check if message has already arrived
        if message not in messages_arrived_K:
            messages_arrived_K.append(message)
            print(f"Messages arrived: {messages_arrived_K}")

            #If 10 messages have arrived
            if len(messages_arrived_K) == 10:
                print("Eteteri recieved 10 messages!")
                send_evacuation_ship()
        
        #If message has already arrived
        else:
            print(f"Message {message} already arrived!")

#Send evacuation ship to island
def send_evacuation_ship():
    global messages_arrived_E
    global messages_arrived_K
    global ship_sent_E
    global ship_sent_K

    #If 10 messages were recieved by Pohteri
    if len(messages_arrived_E) == 10 and ship_sent_K == False:
        print("Evacuation ship sent to islands north part!")
        ship_sent_E = True
        #Send the ship to the island
        start_evacuation_ship_E()

    #If 10 messages were recieved by Eteteri
    if len(messages_arrived_K) == 10 and ship_sent_E == False:
        print("Evacuation ship sent to islands south part!")
        ship_sent_K = True
        #Send the ship to the island
        start_evacuation_ship_K()

#Functions to move the evacuation ships
def move_evacuation_ship_E():
    ship_marker = tk.Label(window, text="Ship")
    ship_marker.place(x=1000, y=185)
    for i in range(100):
        newShipPosition = 1000 - (i*7.7)
        ship_marker.place(x=newShipPosition, y=185)
        window.update()
        t.sleep(0.1)
    playsound(trumpet1)
    count_party_size()

def move_evacuation_ship_K():
    ship_marker = tk.Label(window, text="Ship")
    ship_marker.place(x=1000, y=505)
    for i in range(100):
        newShipPosition = 1000 - (i*7.7)
        ship_marker.place(x=newShipPosition, y=505)
        window.update()
        t.sleep(0.1)
    playsound(trumpet2)
    count_party_size()

#Count party size and amount of pepper needed
def count_party_size():
    global ernesti_monkey_counter
    global kernesti_monkey_counter
    ernesti_party_size = ernesti_monkey_counter*4
    kernesti_party_size = kernesti_monkey_counter*4

    if ernesti_party_size > kernesti_party_size:
        print(f"{ernesti_monkey_counter} of Ernestis monkeys arrived safely!")
        print(f"{kernesti_monkey_counter} of Kernestis monkeys arrived safely!")
        print(f"Ernestis party size has food for {ernesti_party_size} people and it is bigger than Kernestis party size which has food for {kernesti_party_size} people!")

    elif ernesti_party_size < kernesti_party_size:
        print(f"{kernesti_monkey_counter} of Kernestis monkeys arrived safely!")
        print(f"{ernesti_monkey_counter} of Ernestis monkeys arrived safely!")
        print(f"Kernestis party size has food for {kernesti_party_size} people and it is bigger than Ernestis party size which has food for {ernesti_party_size} people!")

    #count amount of pepper needed in parties
    pepper_needed_E = ernesti_monkey_counter*2
    pepper_needed_K = kernesti_monkey_counter*2
    pepper_needed= pepper_needed_E + pepper_needed_K
    print(f"Pepper needed in total: {pepper_needed} teaspoons!")

#####THREADS#####
#Create threads for swimmers
def start_monkey_swim_E():
    threading.Thread(target=monkey_swim_E).start()

def start_monkey_swim_K():
    threading.Thread(target=monkey_swim_K).start()

#Create threads for port guards
def start_port_guard_watch_P(message):
    threading.Thread(target=port_guard_watch_P, args=(message,)).start()

def start_port_guard_watch_E(message):
    threading.Thread(target=port_guard_watch_E, args=(message,)).start()

#Create threads for evacuation ship
def start_evacuation_ship_E():
    threading.Thread(target=move_evacuation_ship_E).start()

def start_evacuation_ship_K():
    threading.Thread(target=move_evacuation_ship_K).start()

#####TKINTER#####
#Set up tkinter window
window = tk.Tk()
window.title("Island Quest")
window.geometry("1300x700+100+100")
#Create canvas
canvas = tk.Canvas(window, width=1300, height=700)
canvas.pack()

create_island(canvas)
create_mainland(canvas)

#####BUTTONS#####
button1 = tk.Button(window, text="E monkey swim", width=10, height=2, command=start_monkey_swim_E)
button1.pack()
button1.place(x=10, y=10)

button2 = tk.Button(window, text="K monkey swim", width=10, height=2, command=start_monkey_swim_K)
button2.pack()
button2.place(x=10, y=50)

button3 = tk.Button(window, text="Teach EM", width=10, height=2, command=teach_message_to_swimmer_E)
button3.pack()
button3.place(x=135, y=10)

button4= tk.Button(window, text="Teach KM", width=10, height=2, command=teach_message_to_swimmer_K)
button4.pack()
button4.place(x=135, y=50)

button5 = tk.Button(window, text="E Send 10 monkeys", width=10, height=2, command=send_10_monkeys_E)
button5.pack()
button5.place(x=260, y=10)

button6 = tk.Button(window, text="K Send 10 monkeys", width=10, height=2, command=send_10_monkeys_K)
button6.pack()
button6.place(x=260, y=50)


#####STATIONARY MARKERS#####
ernesti_marker = tk.Label(window, text="E")
ernesti_marker.place(x=235, y=180)
kernesti_marker = tk.Label(window, text="K")
kernesti_marker.place(x=235, y=500)
pohteri_marker = tk.Label(window, text="P")
pohteri_marker.place(x=1000, y=160)
eteteri_marker = tk.Label(window, text="E")
eteteri_marker.place(x=1000, y=480)

window.mainloop()