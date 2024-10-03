import tkinter as tk
import random
import numpy as np
import matplotlib.pyplot as plt
import threading
import time
import playsound



###GLOBALS###
#Matrix for the pool
pool = np.zeros((20,60))

#Matrix for the trenches
trenchE = np.ones((100,1))
print(trenchE)
trenchK= np.ones((100,1))

#Coordinates for the trench endings
Ae=(460,400)
Be=(464,200)
Ak=(656,400)
Bk=(660,200)

#Sounds
whistleE = "whistleE.wav"
whistleK = "whistleK.wav"
dig = "digsound.wav"

#Monkey locations
monkey_locations = {}

#Fetched monkey
fetched_monkeyE = None
fetched_monkeyK = None

#Forest coordanates
forest = (200, 200, 350, 350)

#Monkeys working
monkeys_workingE = 0
monkeys_workingK = 0

#Cells in trenches
cell_height = 2
trench_cell_map = {}
current_cell = 0

for i in range(100):  # Assuming 100 trench cells
    y_coord = 400 - (i * 2)  # Assuming each trench cell is 2 pixels high
    trench_cell_map[y_coord] = i

print(trench_cell_map)

#Locks
counter_lock_E = threading.Lock()
counter_lock_K = threading.Lock()


###FUNCTIONS###
#Create the world
def canvas_create_world():
    #Fill the sea
    canvas.create_rectangle(0, 0, 1000, 700, fill="lightblue")
    #Create island
    canvas.create_rectangle(200, 200, 800, 500, fill="sandybrown")
    #Create the pool
    canvas.create_rectangle(440, 400, 680, 480, fill="blue")
    #Trench on the left for Ernesti
    canvas.create_rectangle(460, 400, 464, 200, fill="sandybrown", outline="black")
    #Trench on the right for Kernesti
    canvas.create_rectangle(656, 400, 660, 200, fill="sandybrown", outline="black")
    #Create a forest
    canvas.create_rectangle(200, 200, 350, 350, fill="green", outline="green")
    #Ernesti relax area
    canvas.create_rectangle(380, 380, 440, 440, fill="lightgreen")
    #Kernesti relax area
    canvas.create_rectangle(680, 380, 740, 440, fill="lightgreen")

#Add the monkeys
def canvas_create_monkey():
    global monkey_locations
    #create 10 monkeys to forest
    for i in range(10):
        x_random = random.randint(200, 300)
        y_random = random.randint(200, 300)
        monkey = canvas.create_oval(x_random, y_random, x_random+10, y_random+10, fill="brown")
        monkey_locations[i] = (monkey, x_random, y_random)
        print("Monkeylist" , monkey_locations)


#Function for ernesti to fetch a monkey from the forest
def ernesti_fetch_monkey():
    global monkey_locations
    ernesti_whistle()
    move_monkey_threadE(Ae[0]-1, Ae[1]-5) #move monkey to trench, for better visibility dont move to exact Ae lcoation.

def kernesti_fetch_monkey():
    global monkey_locations
    kernesti_whistle()
    move_monkey_threadK(Ak[0]-1, Ak[1]-5) #move monkey to trench, for better visibility dont move to exact Ak lcoation.

#Move the monkey inside thread  
def move_monkeyE(target_x, target_y):
    global monkey_locations, fetched_monkeyE

    print(monkey_locations)
    print("Moving monkey to", target_x, target_y)
        #select a random monkey
    monkey_key = random.choice(list(monkey_locations.keys()))
    monkey_id, current_x, current_y = monkey_locations[monkey_key]

    FOREST_X_START, FOREST_Y_START, FOREST_X_END, FOREST_Y_END = forest

        #Check if the monkey is in the forest
    if current_x >= FOREST_X_START and current_x <= FOREST_X_END and current_y >= FOREST_Y_START and current_y <= FOREST_Y_END:

            #selected monkey is in the forest set up movement
        print("Selected monkey", monkey_id, "at", current_x, current_y)
        steps = 40
        x_step = (target_x - current_x) / steps
        y_step = (target_y - current_y) / steps

        #move the monkey
        for step in range(steps):
            current_x += x_step
            current_y += y_step
            canvas.move(monkey_id, x_step, y_step)
            canvas.update()
            time.sleep(0.1)

        #Change location of the monkey
        monkey_locations[monkey_key] = (monkey_id, target_x, target_y)
        fetched_monkeyE= monkey_locations.pop(monkey_key)
        print("monkeylist after move", monkey_locations)
        return fetched_monkeyE
        
        #if chosen monkey is not in the forest
    else:
        print("Chosen monkey is not lounging around in the forest")

def move_monkeyK(target_x, target_y):
    global monkey_locations, fetched_monkeyK

    print(monkey_locations)
    print("Moving monkey to", target_x, target_y)
    #select a random monkey
    monkey_key = random.choice(list(monkey_locations.keys()))
    monkey_id, current_x, current_y = monkey_locations[monkey_key]

    FOREST_X_START, FOREST_Y_START, FOREST_X_END, FOREST_Y_END = forest

    #Check if the monkey is in the forest
    if current_x >= FOREST_X_START and current_x <= FOREST_X_END and current_y >= FOREST_Y_START and current_y <= FOREST_Y_END:

        #selected monkey is in the forest set up movement
        print("Selected monkey", monkey_id, "at", current_x, current_y)
        steps = 40
        x_step = (target_x - current_x) / steps
        y_step = (target_y - current_y) / steps

        #move the monkey
        for step in range(steps):
            current_x += x_step
            current_y += y_step
            canvas.move(monkey_id, x_step, y_step)
            canvas.update()
            time.sleep(0.1)

        #Change location of the monkey
        monkey_locations[monkey_key] = (monkey_id, target_x, target_y)
        fetched_monkeyK= monkey_locations.pop(monkey_key)
        print("monkeylist after move", monkey_locations)
        return fetched_monkeyK
    
    #if chosen monkey is not in the forest
    else:
        print("Chosen monkey is not lounging around in the forest")

#Create function to order monkey to dig
def monkey_digE():
    global fetched_monkeyE, trenchE
    
    if fetched_monkeyE is None:
        print("No monkey fetched")
        return
    
    
    monkey_id, current_x, current_y = fetched_monkeyE
    print(monkey_id, current_x, current_y)
    monkey_counterE()

    for i in range(len(trenchE)):
        trenchE[i] -= 1
        plot_matrices()
        current_x = 460
        current_y = 400 - (i * 2)
        fetched_monkeyE = (monkey_id, current_x, current_y)

        canvas.move(monkey_id, 0, -2)
        canvas.update()
        play_dig_sound()
        time.sleep(2)

def monkey_digK():
    global fetched_monkeyK, trenchK
    
    if fetched_monkeyK is None:
        print("No monkey fetched")
        return
    
    monkey_id, current_x, current_y = fetched_monkeyK
    print(monkey_id, current_x, current_y)
    monkey_counterK()

    for i in range(len(trenchK)):
        trenchK[i] = 0
        plot_matrices()
        current_x = 460
        current_y = 200 - (i * 2)


        canvas.move(monkey_id, 0, -2)
        canvas.update()
        play_dig_sound()
        time.sleep(2**i)

            

#Make matrices visible with ai help
def plot_pool():
    pool_x_start, pool_y_start = 440, 400
    pool_x_end, pool_y_end = 680, 480
    pool_width = pool_x_end - pool_x_start
    pool_height = pool_y_end - pool_y_start

    #setip cells
    cell_width = pool_width / pool.shape[1]
    cell_height = pool_height / pool.shape[0]

    #plot the pool
    for row in range(pool.shape[0]):
        for col in range(pool.shape[1]):
            color = "white" if pool[row, col] == 0 else "blue"
            x0 = pool_x_start + col * cell_width
            y0 = pool_y_start + row * cell_height
            x1 = x0 + cell_width
            y1 = y0 + cell_height
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white")

def plot_matrices():
    #plot the trenches
    trench_width = 1
    for i in range(100):
        colorE = "sandybrown" if trenchE[i] == 1 else "black"
        canvas.create_rectangle(460, 400 - i * 2, 464, 400 - (i+1) * 2 - trench_width, fill=colorE,outline="black")

        colorK = "sandybrown" if trenchK[i] == 1 else "black"
        canvas.create_rectangle(656, 400 - i * 2, 660, 400 - (i+1) * 2 - trench_width, fill=colorK,outline="black")
    
    canvas.update()

def fetch_assistant_monkeyE():
    global fetched_monkeyE, monkeys_workingE, monkey_locations, cell_height
    print(fetched_monkeyE)
    if fetched_monkeyE is None:
        print("No monkey to help")
        return
    else:
        ernesti_whistle()
        print("Fetching assistant monkey")
        
        monkey_key=random.choice(list(monkey_locations.keys()))
        monkey_id, current_x, current_y = monkey_locations[monkey_key]
        last_monkey_id, last_x, last_y = fetched_monkeyE

        FOREST_X_START, FOREST_Y_START, FOREST_X_END, FOREST_Y_END = forest

        #Check if the monkey is in the forest
        if current_x >= FOREST_X_START and current_x <= FOREST_X_END and current_y >= FOREST_Y_START and current_y <= FOREST_Y_END:
            print("Selected monkey", monkey_id, "at", current_x, current_y)
            steps = 40
            x_step = (last_x - current_x) / steps
            y_step = (last_y - current_y - (10*2)) / steps

            #move the monkey
            for step in range(steps):
                current_x += x_step
                current_y += y_step
                canvas.move(monkey_id, x_step, y_step)
                canvas.update()
                time.sleep(0.1)

            #Change location of the monkey
            monkey_locations[monkey_key] = (monkey_id, current_x, current_y)
            fetched_monkeyE = monkey_locations.pop(monkey_key)
            
            monkey_work_id, work_x, work_y = fetched_monkeyE
            initial_dig_y = work_y

            for i in range(len(trenchE)):
                print("Working on trench", i)
                

                work_x = 460
                work_y = initial_dig_y - (i * 2)
                cell=check_trench_cell(work_y)
                print("before", cell)
                trenchE[cell] -= 1
                plot_matrices()
                cell -= 1
                print("after", cell)
                print("Monkey working at", work_x, work_y)
                fetched_monkeyE = (monkey_work_id, work_x, work_y)

                canvas.move(monkey_work_id, 0, -2)
                canvas.update()
                play_dig_sound()
                #Apply exponential sleep time
                time.sleep(2**i)

def fetch_assistant_monkeyK():
    global fetched_monkeyK, monkeys_workingK, monkey_locations, cell_height
    print(fetched_monkeyK)
    if fetched_monkeyK is None:
        print("No monkey to help")
        return
    else:
        kernesti_whistle()
        print("Fetching assistant monkey")
        
        monkey_key=random.choice(list(monkey_locations.keys()))
        monkey_id, current_x, current_y = monkey_locations[monkey_key]
        last_monkey_id, last_x, last_y = fetched_monkeyK

        FOREST_X_START, FOREST_Y_START, FOREST_X_END, FOREST_Y_END = forest

        #Check if the monkey is in the forest
        if current_x >= FOREST_X_START and current_x <= FOREST_X_END and current_y >= FOREST_Y_START and current_y <= FOREST_Y_END:
            print("Selected monkey", monkey_id, "at", current_x, current_y)
            steps = 40
            x_step = (last_x - current_x) / steps
            y_step = (last_y - current_y - (10*2)) / steps

            #move the monkey
            for step in range(steps):
                current_x += x_step
                current_y += y_step
                canvas.move(monkey_id, x_step, y_step)
                canvas.update()
                time.sleep(0.1)

            #Change location of the monkey
            monkey_locations[monkey_key] = (monkey_id, current_x, current_y)
            fetched_monkeyK = monkey_locations.pop(monkey_key)
            
            monkey_work_id, work_x, work_y = fetched_monkeyK
            initial_dig_y = work_y

            for i in range(len(trenchK)):
                print("Working on trench", i)
                

                work_x = 460
                work_y = initial_dig_y - (i * 2)
                cell=check_trench_cell(work_y)
                print("before", cell)
                trenchK[cell] -= 1
                plot_matrices()
                cell -= 1
                print("after", cell)
                print("Monkey working at", work_x, work_y)
                fetched_monkeyK = (monkey_work_id, work_x, work_y)

                canvas.move(monkey_work_id, 0, -2)
                canvas.update()
                play_dig_sound()
                #Apply exponential sleep time
                time.sleep(2**i)
        
        #if chosen monkey is not in the forest
        else:
            print("Chosen monkey is not lounging around in the forest")

#Check coordinate of cells in trench
def check_trench_cell(y_coord):
    global trench_cell_map, current_cell
    #round y_coord to nearest int
    # Rounding the y_coord to the nearest even number that represents a trench cell's y-coordinate
    rounded_y = int(round(y_coord / cell_height) * cell_height)
    print(f"Rounded y-coordinate: {rounded_y}")

    # Find the corresponding trench cell from the trench_cell_map
    if rounded_y in trench_cell_map:
        current_cell = trench_cell_map[rounded_y]
        return current_cell
    else:
        print(f"y-coordinate {rounded_y} is not in the trench cell map.")




def monkey_counterE():
    global monkeys_workingE
    with counter_lock_E:
        monkeys_workingE += 1
        print("Monkeys working", monkeys_workingE)

def monkey_counterK():
    global monkeys_workingK
    with counter_lock_K:
        monkeys_workingK += 1
        print("Monkeys working", monkeys_workingK)


###THREADS###
def ernesti_whistle():
    threading.Thread(target=playsound.playsound, args=(whistleE,)).start()

def kernesti_whistle():
    threading.Thread(target=playsound.playsound, args=(whistleK,)).start()

def move_monkey_threadE(target_x, target_y):
    threading.Thread(target=move_monkeyE, args=(target_x, target_y)).start()

def move_monkey_threadK(target_x, target_y):
    threading.Thread(target=move_monkeyK, args=(target_x, target_y)).start()

def monkey_dig_threadE():
    threading.Thread(target=monkey_digE).start()

def monkey_dig_threadK():
    threading.Thread(target=monkey_digK).start()

def play_dig_sound():
    threading.Thread(target=playsound.playsound(dig)).start()

def fetch_assistant_monkey_threadE():
    threading.Thread(target=fetch_assistant_monkeyE).start()


### SETIP TKINTER WINDOW ##
window = tk.Tk()
window.title("Island Quest 2")
window.geometry("1000x700")

###SETUP CANVAS ###
canvas= tk.Canvas(window, height=700, width=1000)
canvas.pack()
canvas_create_world()
canvas_create_monkey()
plot_pool()
plot_matrices()

###STATIONARY MARKERS###
ernesti_marker = tk.Label(window, text="E")
ernesti_marker.place(x=400, y=410)
kernesti_marker = tk.Label(window, text="K")
kernesti_marker.place(x=710, y=410)
ernesti_Ae = tk.Label(window, text="Ae")
ernesti_Ae.place(x=Ae[0], y=Ae[1])

###BUTTONS###
button1 = tk.Button(window, text="Ernesti fetch monkey", command=ernesti_fetch_monkey)
button1.place(x=10, y=10)
button2 = tk.Button(window, text="Ernesti command monkey to dig", command=monkey_dig_threadE)
button2.place(x=10, y=40)
button3 = tk.Button(window, text="Kernesti fetch monkey", command=kernesti_fetch_monkey)
button3.place(x=10, y=70)
button4 = tk.Button(window, text="Kernesti command monkey to dig", command=monkey_dig_threadK)
button4.place(x=10, y=100)
button5 = tk.Button(window, text="Fetch assistant monkey", command=fetch_assistant_monkey_threadE)
button5.place(x=10, y=130)
button6 = tk.Button(window, text="Fetch assistant monkey", command=fetch_assistant_monkeyK)
button6.place(x=10, y=160)

window.mainloop()