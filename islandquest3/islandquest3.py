import tkinter as tk
import random
import threading
import time
import pygame
import winsound


###GLOBALS###
#Island positions
island_positions = []
island_count = 1

#Initialize pygame mixer
pygame.mixer.init()

#Sounds
explosion_sound = "explosion.wav"
laugh_sound = "laugh.wav"
crunch_sound = "crunch.wav"
splash_sound = "splash.wav"

#Monkey sounds list
monkey_sound_timers = []

#Monkeylist
monkey_list = []

#Event for reset
reset_event = threading.Event()

###TKINTER###
window = tk.Tk()
window.title("Island Quest 3")
window.geometry("1500x1000")



###THREADS###
def thread_explosion():
    threading.Thread(target=play_explosion).start()

def thread_random_sound():
    threading.Thread(target=random_sound).start()

def thread_add_monkeys(random_x, random_y, island_size, island_name):
    threading.Thread(target=add_monkeys, args=(random_x, random_y, island_size, island_name)).start()

def thread_play_laugh_sound():
    threading.Thread(target=play_laugh_sound).start()

def play_monkey_sound():
    #Check if reset
    if reset_event.is_set():
        for timer in monkey_sound_timers:
            timer.cancel()
        return
    #Play random monkey sound every 10 seconds
    else:
        random_sound() 
        timer=threading.Timer(10, play_monkey_sound)
        timer.start()
        monkey_sound_timers.append(timer)

def thread_monkey_survival_island():
    threading.Thread(target=monkey_survival_island).start()

def thread_monkey_death(monkey):
    threading.Thread(target=monkey_death, args=(monkey,)).start()

def thread_count_monkeys(island):
    threading.Thread(target=display_monkey_number, args=(island,)).start()

def thread_travel_island_swim(island):
    threading.Thread(target=travel_island_swim, args=(island,)).start()
    
def thread_move_monkey(monkey, direction):
    if reset_event.is_set():
        return
    else:
        threading.Thread(target=move_monkey, args=(monkey, direction)).start()

def thread_play_crunch_sound():
    threading.Thread(target=play_crunch_sound).start()

def thread_play_swim_sound():
    threading.Thread(target=play_swim_sound).start()

###FUNCTIONS###
#Create sea
def draw_sea():
    canvas.create_rectangle(0, 0, 1500, 1000, fill="lightblue")

#Create island
def volcanic_activity():
    global island_count, island_positions
    #Adjust island size for consistency
    islandSize = random.randint(130, 180)

    canvas_width = 1500
    canvas_height = 1000
    
    #Calculate grid cell size
    grid_cols = 5  
    grid_rows = 2
    grid_cell_width = canvas_width // grid_cols
    grid_cell_height = canvas_height // grid_rows

    #Attempts tracked to prevent infinite loop
    attempts = 0
    while attempts < 100:
    
        #Randomly place
        random_col = random.randint(0, grid_cols - 1)
        random_row = random.randint(0, grid_rows - 1)
        
        #Calculate random x and y
        randomX = random_col * grid_cell_width + random.randint(0, grid_cell_width - islandSize)
        randomY = random_row * grid_cell_height + random.randint(0, grid_cell_height - islandSize)
        

        if check_island_location(randomX, randomY, islandSize) == False:
            reset_event.clear()
            #Store island position
            islandName = f"S{island_count}"
            monkeyCount = 0

            #Setup island dictionary
            island = {
                "x": randomX, 
                "y": randomY, 
                "size": islandSize, 
                "name": islandName, 
                "monkeys": monkeyCount,
                "travel": False
                }
            island_positions.append(island)
            print(island_positions)

            #Play island creation sound
            thread_explosion()
 
            #Create a rectangular island
            canvas.create_rectangle(randomX, randomY, randomX + islandSize, randomY + islandSize, fill="darkgreen", outline="sandybrown", width=5, tags=islandName)

            #Display island name
            canvas.create_text(randomX + islandSize // 2, randomY + islandSize // 2, text=islandName, font=("Arial", 16), tags="island_name")
            island_count += 1
            
            #Add monkeys
            thread_add_monkeys(randomX, randomY, islandSize, islandName)
            break
        
        attempts += 1
    
#Check if island for not overlapping, this required AI help for the counting method
def check_island_location(new_x, new_y, new_size):
    #Iterate through existing islands
    for island in island_positions:
        existing_x = island["x"]
        existing_y = island["y"]
        existing_size = island["size"]

        distance = ((new_x - existing_x) ** 2 + (new_y - existing_y) ** 2) ** 0.5
        if distance < new_size + existing_size:
            return True
    return False

#Explosion effect
def play_explosion():
    pygame.mixer.Sound(explosion_sound).play()

#Play laugh sound
def play_laugh_sound():
    pygame.mixer.Sound(laugh_sound).play()

#Play crunch sound
def play_crunch_sound():
    pygame.mixer.Sound(crunch_sound).play()

#Random sound effect
def random_sound():
    frequency = random.randint(400, 2000)
    duration = 250
    winsound.Beep(frequency, duration)

#Swim sound
def play_swim_sound():
    pygame.mixer.Sound(splash_sound).play()   

#Add monkeys to new island
def add_monkeys(island_x, island_y, island_size, island_name):
    global monkey_list

    #Add 10 monkeys to the island
    for i in range(10):
        #Check for reset
        if reset_event.is_set():
            return
        else:
            #Randomly place monkey on island
            x = random.randint(island_x, island_x + island_size -10)
            y = random.randint(island_y, island_y + island_size -10)
            #Add specific monkey tag
            monkey_tag = f"monkey_{len(monkey_list) + 1}"
            canvas.create_text(x, y, text="🐒", font=("Arial", 13), tags=monkey_tag,)
            #Create monkey dictionary
            monkey = {
                "monkeyID": len(monkey_list) + 1,
                "monkeyX": x,
                "monkeyY": y,
                "monkeyIsland": island_name,
                "monkeyStatus": True,
                "canvasTag": monkey_tag,
                "swimming": False,
                "monkeyDeathEvent": threading.Event()
            }
            monkey_list.append(monkey)
            #Play monkey sound
            play_monkey_sound()
            thread_monkey_death(monkey)
            time.sleep(0.1)
    thread_count_monkeys(island_name)
    print(monkey_list)

#Reset functions
#Main reset function
def reset_main():
    global reset_event, monkey_sound_timers
    reset_event.set()
    clear_counters()
    remove_islands()
    clear_piers()
    remove_monkeys()
    remove_island_names()
    for timer in monkey_sound_timers:
        timer.cancel()
    print(monkey_list)
    print(island_positions)

#Remove monkeys
def remove_monkeys():
    global monkey_list
    for monkey in monkey_list[:]:
        canvas.delete(monkey["canvasTag"])
    monkey_list.clear()

#Remove island names
def remove_island_names():
    canvas.delete("island_name")

#Remove islands
def remove_islands():
    global island_positions, island_count
    island_count = 1

    #Iterate through islands to remove all
    for island in island_positions[:]:
        name = island["name"] 
        print(name)
        canvas.delete(name)
        print(island_positions)
        print(island_positions)
    island_positions.clear()

#Clear monkey counters for reset
def clear_counters():
    global island_positions
    for island in island_positions:
        island["monkeys"] = 0
        print(island["name"]+"_monkeys")
        canvas.delete(island["name"]+"_monkeys")

#Clear piers for reset
def clear_piers():
    canvas.delete("pier")

#Check if monkey is on island, for debugging purposes
def check_monkey_position():
    global monkey_list, island_positions
    print(monkey_list)
    print(island_positions)
    for monkey in monkey_list:
        print("checking monkey")
        monkey_id=monkey["monkeyID"]
        x = monkey["monkeyX"]
        y = monkey["monkeyY"]
        monkey_island = monkey["monkeyIsland"]
        monkey["monkeyStatus"] = False

        for island in island_positions:
            print(island)
            island_name = island["name"]
            island_x = island["x"]
            island_y = island["y"]
            island_size = island["size"]
            if monkey_island == island_name and island_x <= x <=island_x + island_size and island_y <= y <= island_y + island_size:
                monkey["monkeyStatus"] = True
                print(f"Monkey {monkey['monkeyID']} is on the island {island_name}")
                break

        if not monkey["monkeyStatus"]:
            monkey["monkeyStatus"] = False
            print(f"Monkey {monkey['monkeyID']} has left the island")

#Monkeystatus check for debugging purposes
def monkey_survival_island():
    global monkey_list
    for monkey in monkey_list:
        if monkey["monkeyStatus"]:
            print(f"Monkey {monkey['monkeyID']} is safe")
        else:
            print("Monkey has left the island")    
            break


def monkey_death(monkey):
    global monkey_list
    if reset_event.is_set():
        return
    else:
        while not monkey["monkeyDeathEvent"].is_set():
            if reset_event.is_set():
                break
            else:
                if monkey["monkeyStatus"]:
                    island_survival_chance(monkey)
                else:
                    sea_survival_chance(monkey)
        
#Island survival chance
def island_survival_chance(monkey):
    global monkey_list
    #Check for reset
    if reset_event.is_set():
        return
    else:
        #print("monkeys on island fighting for survival")
        #1% chance of monkey dying every 10 seconds
        if random.randint(1, 100) == 1:
            thread_play_laugh_sound()
            print(f"Monkey {monkey['monkeyID']} has died")
            island = monkey["monkeyIsland"]
            monkey["monkeyDeathEvent"].set()
            monkey_list.remove(monkey)
            canvas.delete(monkey["canvasTag"])
            print(monkey_list)
            
            #Update monkey count
            display_monkey_number(island)
        time.sleep(10)

#Sea survival chance
def sea_survival_chance(monkey):
    global monkey_list
    #Check for reset
    if reset_event.is_set():
        return
    else:
        if monkey["swimming"]:
            #1% chance of monkey dying every 1 second
            print("monkeys at sea fighting for survival")
            if random.randint(1, 100) == 1:
                thread_play_crunch_sound()        
                print(f"Monkey {monkey['monkeyID']} has died at sea")
                monkey["swimming"] = False
                monkey_list.remove(monkey)
                canvas.delete(monkey["canvasTag"])
                print(monkey_list)
                monkey["monkeyDeathEvent"].set() 
            time.sleep(1)
        #else:
            #time.sleep(1000000000)

#Move monkey to middle of the sea
def send_monkey_to_sea():
    global monkey_list

    #Select random monkey
    random_monkey = random.choice(monkey_list)
    random_monkey["monkeyStatus"] = False
    random_monkey["swimming"] = True
    print(f"Monkey {random_monkey['monkeyID']} has left to sea")
    #New coordinates
    random_monkey["monkeyX"] = 1500 // 2
    random_monkey["monkeyY"] = 1000 // 2
    island_name = random_monkey["monkeyIsland"]
    random_monkey["monkeyIsland"] = "Sea"
    #Update monkey location
    canvas.coords(random_monkey["canvasTag"], random_monkey["monkeyX"], random_monkey["monkeyY"])
    canvas.tag_raise(random_monkey["canvasTag"])
    canvas.update()
    #Update monkey count
    display_monkey_number(island_name)

#Monkey amount on island
def display_monkey_number(island_name):
    global monkey_list, island_positions
    monkeys_on_island = 0
    #Iterate trough monkeys to count monkeys on island
    for monkey in monkey_list:
        if island_name == monkey["monkeyIsland"]:
            monkeys_on_island += 1

    for i, island_data in enumerate(island_positions):
        if island_data["name"] == island_name:
            island_data["monkeys"] = monkeys_on_island
            break

    #Clear previous monkey count    
    canvas.delete(island_data["name"]+"_monkeys")

    print(island_positions)
    print(f"Total monkeys on island: {monkeys_on_island}")
    print(island_data)

    #Display monkey count
    canvas.create_text(island_data["x"] + island_data["size"], island_data["y"] + island_data["size"], text=f"Monkeys: {monkeys_on_island}", font=("Arial", 8), anchor="se", tags=island_data["name"]+"_monkeys")

#Start monkey swimming
def check_if_travel():
    global island_positions
    for island in island_positions:
        #Set S1 to know about travelling
        if island["name"] == "S1":
            island["travel"] = True
        if island["travel"]:
            print(f"Island {island['name']} knows about travelling")
            travel_island(island)
        else:
            print(f"Island {island['name']} does not know about travelling")

#If island knows about travelling, create piers
def travel_island(island):
    island_x = island["x"]
    island_y = island["y"]
    island_size = island["size"]
    pier_length = 50

    #Create north pier
    canvas.create_line(island_x + island_size // 2, island_y, island_x + island_size // 2, island_y - pier_length, fill="black", width=5, tags="pier")

    #Create south pier
    canvas.create_line(island_x + island_size // 2, island_y + island_size, island_x + island_size // 2, island_y + island_size + pier_length, fill="black", width=5, tags="pier")

    #Create east pier
    canvas.create_line(island_x + island_size, island_y + island_size // 2, island_x + island_size + pier_length, island_y + island_size // 2, fill="black", width=5, tags="pier")

    #Create west pier
    canvas.create_line(island_x, island_y + island_size // 2, island_x - pier_length, island_y + island_size // 2, fill="black", width=5, tags="pier")

    print(f"Island {island['name']} has piers")
    #Start monkey swimming
    thread_travel_island_swim(island)

#Move monkey to end of the pier and choose random direction
def travel_island_swim(island):
    global monkey_list, reset_event
    #Check for reset
    if reset_event.is_set():
        return
    else:
        #List of monkeys on island that knows about travelling
        
        while island["travel"]:
            #Check for reset
            monkeys_ready_to_swim = [monkey for monkey in monkey_list if monkey["monkeyIsland"] == island["name"]]
            if reset_event.is_set():
                break
            else:
                if monkeys_ready_to_swim:
                    #monkeys_ready_to_swim = [monkey for monkey in monkey_list if monkey["monkeyIsland"] == island["name"]]
                    #Select random monkey
                    random_monkey = random.choice(monkeys_ready_to_swim)
                    random_monkey["monkeyIsland"] = "Sea"
                    random_monkey["monkeyStatus"] = False
                    random_monkey["swimming"] = True
                    #Update monkey count
                    display_monkey_number(island["name"])
                    monkey_id = random_monkey["monkeyID"]
                    direction = random.choice(["north", "south", "east", "west"])
                    #Move monkey to end of the chosen pier
                    if direction == "north":
                        random_monkey["monkeyY"] = island["y"] - 50
                        random_monkey["monkeyX"] = island["x"] + island["size"] // 2
                    elif direction == "south":
                        random_monkey["monkeyY"] = island["y"] + island["size"] + 50
                        random_monkey["monkeyX"] = island["x"] + island["size"] // 2
                    elif direction == "east":
                        random_monkey["monkeyX"] = island["x"] + island["size"] + 50
                        random_monkey["monkeyY"] = island["y"] + island["size"] // 2
                    elif direction == "west":
                        random_monkey["monkeyX"] = island["x"] - 50
                        random_monkey["monkeyY"] = island["y"] + island["size"] // 2

                    #Update monkey loction to end of the pier
                    canvas.coords(random_monkey["canvasTag"], random_monkey["monkeyX"], random_monkey["monkeyY"])
                    canvas.tag_raise(random_monkey["canvasTag"])
                    canvas.update()
                    #Play swim sound once to indicate monkey is swimming, saves everyones hearing to play it once rather than on every step
                    play_swim_sound()
                    #thread_move_monkey(random_monkey, direction)
                    print(f"Monkey {monkey_id} is swimming to the {direction}")
                    #Start moving monkey to the chosen direction
                    thread_move_monkey(random_monkey, direction)
                    #Remove monkey from list of monkeys ready to swim
                    monkeys_ready_to_swim.remove(random_monkey)
                    time.sleep(10)
                else:
                    break

""" did not work as intended, the did not monkeys start swimming when the island ran out of monkeys and then got more
def keep_swimming(island):
    print(island)
    while island["monkeys"] == 0:
        travel_island_swim(island)
        time.sleep(1)
"""
        
                
#Move monkey to chosen direction
def move_monkey(monkey, direction):
    global reset_event
    #Check for reset
    if reset_event.is_set():
        return
    else:
        #Setup movement variables
        speed = 5
        travel_distance = 2000
        current_distance = 0
        #Move monkey
        while current_distance < travel_distance:
            #Check for reset
            if reset_event.is_set():
                break
            #Break if monkeystatus is true to check if monkey has reached land
            if monkey["monkeyStatus"]:
                break
            #Move monkey in chosen direction
            if direction == "north":
                if monkey["monkeyStatus"] == False:
                    canvas.move(monkey["canvasTag"], 0, -speed)
                    monkey["monkeyY"] -= speed
            elif direction == "south":
                if monkey["monkeyStatus"] == False:
                    canvas.move(monkey["canvasTag"], 0, speed)
                    monkey["monkeyY"] += speed
            elif direction == "east":
                if monkey["monkeyStatus"] == False:
                    canvas.move(monkey["canvasTag"], speed, 0)
                    monkey["monkeyX"] += speed
            elif direction == "west":
                if monkey["monkeyStatus"] == False:
                    canvas.move(monkey["canvasTag"], -speed, 0)
                    monkey["monkeyX"] -= speed
            #Fire function for checking if monkey has reached land
            check_if_monkey_finds_land(monkey)
            time.sleep(0.1)

def check_if_monkey_finds_land(monkey):
    global island_positions
    #Iterate through islands to check if monkey has reached land
    for island in island_positions:
        island_name = island["name"]
        island_x = island["x"]
        island_y = island["y"]
        island_size = island["size"]
        island_monkey_count = island["monkeys"]
        if island_x <= monkey["monkeyX"] <= island_x + island_size and island_y <= monkey["monkeyY"] <= island_y + island_size and monkey["monkeyStatus"] == False:
            print(f"Monkey {monkey['monkeyID']} has reached {island_name}")
            if island["travel"]:
                print(f"Monkey {monkey['monkeyID']} has reached {island_name}, island already knows about travelling")
                monkey["monkeyIsland"] = island_name
                monkey["monkeyStatus"] = True
                """ This part makes sure the monkeys dont stop swimming if the island runs empty and then gets more monkeys, but it bugs out the whole thing
                if island_monkey_count < 10:
                    display_monkey_number(island_name)
                    travel_island_swim(island)
                """
                display_monkey_number(island_name)
                break
                
            else:
                print(f"Monkey {monkey['monkeyID']} has reached {island_name}, island does yet not know about travelling")
                monkey["monkeyIsland"] = island_name
                monkey["monkeyStatus"] = True
                island["travel"] = True
                print(island)
                print(island_positions)
                display_monkey_number(island_name)
                travel_island(island)
                break


###CANVAS###
canvas = tk.Canvas(window, width=1500, height=1000)
canvas.pack()
draw_sea()


###BUTTONS###
button1 = tk.Button(window, text="Volcanoes", width=10, height=2, command=volcanic_activity)
button1.place(x=10, y=10)
button2 = tk.Button(window, text="Reset", width=10, height=2, command=reset_main)
button2.place(x=10, y=60)
button3 = tk.Button(window, text="DEBUG Check", width=10, height=2, command=check_monkey_position)
button3.place(x=1400, y=60)
button4 = tk.Button(window, text="DEBUG Surv", width=10, height=2, command=thread_monkey_survival_island)
button4.place(x=1400, y=10)
button5 = tk.Button(window, text="Monkey to Sea", width=15, height=2, command=send_monkey_to_sea)
button5.place(x=10, y=110)
button6 = tk.Button(window, text="Start swimming", width=15, height=2, command=check_if_travel)
button6.place(x=10, y=160)

window.mainloop()