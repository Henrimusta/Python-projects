import tkinter as tk
import random
import numpy as np
import threading
import time
import playsound

###GLOBALS###
#Matrix for the pool
pool = np.zeros((20,60))

#Matrix for the trenches
trenchE = np.ones((100,1))
trenchK= np.ones((100,1))

#Coordinates for the trench endings
Ae=(460,400)
Be=(464,200)
Ak=(656,400)
Bk=(660,200)

#Sounds
whistleE = "whistleE.wav"
whistleK = "whistleK.wav"
digsound = "digsound.wav"

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

#Trench in sections
trenchE_sections = []
trenchK_sections = []

#Thread stopping
stop_threads = threading.Event()

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
    for i in range(20):
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
    if stop_threads.is_set():
        stop_threads.clear()

    print(monkey_locations)
    print("Moving monkey to", target_x, target_y)
    FOREST_X_START, FOREST_Y_START, FOREST_X_END, FOREST_Y_END = forest 

    while True:   
        #select a random monkey
        monkey_key = random.choice(list(monkey_locations.keys()))
        monkey_id, current_x, current_y = monkey_locations[monkey_key]

        #Check if the monkey is in the forest
        if current_x >= FOREST_X_START and current_x <= FOREST_X_END and current_y >= FOREST_Y_START and current_y <= FOREST_Y_END:

            #selected monkey is in the forest set up movement
            print("Selected monkey", monkey_id, "at", current_x, current_y)
            steps = 5
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
            fetched_monkeyE= (monkey_id, target_x, target_y)
            print("monkeylist after move", monkey_locations)
            return fetched_monkeyE
            
            #if chosen monkey is not in the forest
        else:
            print("Chosen monkey is not lounging around in the forest")

def move_monkeyK(target_x, target_y):
    global monkey_locations, fetched_monkeyK
    if stop_threads.is_set():
        stop_threads.clear()

    print(monkey_locations)
    print("Moving monkey to", target_x, target_y)
    FOREST_X_START, FOREST_Y_START, FOREST_X_END, FOREST_Y_END = forest
    
    
    while True:
        #select a random monkey
        monkey_key = random.choice(list(monkey_locations.keys()))
        monkey_id, current_x, current_y = monkey_locations[monkey_key]

        #Check if the monkey is in the forest
        if current_x >= FOREST_X_START and current_x <= FOREST_X_END and current_y >= FOREST_Y_START and current_y <= FOREST_Y_END:

            #selected monkey is in the forest set up movement
            print("Selected monkey", monkey_id, "at", current_x, current_y)
            steps = 5
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
            fetched_monkeyK = (monkey_id, target_x, target_y)
            print("monkeylist after move", monkey_locations)
            return fetched_monkeyK
        
        #if chosen monkey is not in the forest
        else:
            print("Chosen monkey is not lounging around in the forest")

#Create function to order monkey to dig
def monkey_digE():
    global fetched_monkeyE, trenchE, monkey_sleep
    if stop_threads.is_set():
        stop_threads.clear()
    
    if fetched_monkeyE is None:
        print("No monkey fetched")
        return
    
    
    monkey_id, current_x, current_y = fetched_monkeyE
    print(monkey_id, current_x, current_y)
    

    for i in range(len(trenchE)):
        if stop_threads.is_set():
            break
        trenchE[i] -= 1
        plot_matrices()
        current_x = 460
        current_y = 400 - (i * 2)
        fetched_monkeyE = (monkey_id, current_x, current_y)
        play_dig_sound()
        canvas.move(monkey_id, 0, -2)
        canvas.update()
        
        time.sleep(2 ** (i - 1))

def monkey_digK():
    global fetched_monkeyK, trenchK
    if stop_threads.is_set():
        stop_threads.clear()
    
    if fetched_monkeyK is None:
        print("No monkey fetched")
        return
    
    monkey_id, current_x, current_y = fetched_monkeyK
    print(monkey_id, current_x, current_y)

    for i in range(len(trenchK)):
        if stop_threads.is_set():
            break
        trenchK[i] = 0
        plot_matrices()
        current_x = 460
        current_y = 200 - (i * 2)


        canvas.move(monkey_id, 0, -2)
        canvas.update()
        play_dig_sound()
        time.sleep(2 ** (i - 1))

            

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
    global fetched_monkeyE, monkeys_workingE, monkey_locations, cell_height, stop_threads
    print(fetched_monkeyE)
    if stop_threads.is_set():
        stop_threads.clear()

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
            steps = 10
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
            fetched_monkeyE = (monkey_id, current_x, current_y)
            
            monkey_work_id, work_x, work_y = fetched_monkeyE
            initial_dig_y = work_y

            for i in range(len(trenchE)):
                if stop_threads.is_set():
                    break
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
                time.sleep(2 ** (i - 1))

def fetch_assistant_monkeyK():
    global fetched_monkeyK, monkeys_workingK, monkey_locations, cell_height, stop_threads
    print(fetched_monkeyK)
    if stop_threads.is_set():
        stop_threads.clear()

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
            steps = 10
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
            fetched_monkeyK = (monkey_id, current_x, current_y)
            
            monkey_work_id, work_x, work_y = fetched_monkeyK
            initial_dig_y = work_y

            for i in range(len(trenchK)):
                if stop_threads.is_set():
                    break
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
                time.sleep(2 ** (i - 1))
        
        #if chosen monkey is not in the forest
        else:
            print("Chosen monkey is not lounging around in the forest")

#Check coordinate of cells in trench
def check_trench_cell(y_coord):
    global trench_cell_map, current_cell

    #Round y_coord to nearest int
    rounded_y = int(round(y_coord / cell_height) * cell_height)

    #Find the corresponding trench cell from the trench_cell_map
    if rounded_y in trench_cell_map:
        current_cell = trench_cell_map[rounded_y]
        return current_cell
    else:
        print("Coordinate not in trench")

#Reset the monkeys and trenches
def reset():
    global trencE, trenchK, stop_threads
    #Stop all threads
    stop_threads.set()

    #Fill the trenches
    trenchE[:] = 1
    trenchK[:] = 1
    plot_matrices()

    #Call for monkeys to be reset
    kill_and_respawn_monkey()

#Reset the monkeys
def kill_and_respawn_monkey():
    global monkey_locations, forest
    
    #Forest boundaries
    FOREST_X_START, FOREST_Y_START, FOREST_X_END, FOREST_Y_END = forest
    
    #Iterate over the monkeys
    for monkey_id in list(monkey_locations.keys()):
        monkey, x, y = monkey_locations[monkey_id]

        #Check if the monkey is outside the forest
        if x < FOREST_X_START or x > FOREST_X_END or y < FOREST_Y_START or y > FOREST_Y_END:

            #Generate new random coordinates inside the forest
            new_x = random.randint(FOREST_X_START, FOREST_X_END)
            new_y = random.randint(FOREST_Y_START, FOREST_Y_END)
            
            #Move monkey back to forest
            canvas.coords(monkey, new_x, new_y, new_x + 10, new_y + 10)
            
            #Update monkey location
            monkey_locations[monkey_id] = (monkey, new_x, new_y)
            window.update()

#Cut trench in even pieces
def divide_trenchE():
    global trenchE_sections
    start_y = 400
    section_height = 20

    #Divide the trench into 10 sections
    for i in range(10):
        end_y = start_y - section_height + 1
        section_id = i + 1
        trenchE_sections.append((section_id, start_y, end_y))
        start_y -= section_height

    print(trenchE_sections)

    #Call for sending first monkey
    send_first_monkey_of_ten()

#Send the first monkey to random location along the trench
def send_first_monkey_of_ten():
    global trenchE , trenchE_sections, monkey_locations
    random_location=random.randint(200, 400)

    #Use move monkey thread
    move_monkey_threadE(Ae[0]-1, random_location)

    #Call for small delay
    create_small_delay_tread(random_location)
    
#Create small delay to avoid first and second monkey to collide
def create_small_delay(random_location):
    time.sleep(1)
    check_wich_section(random_location)

#Check which section the monkey is in
def check_wich_section(random_location):
    global trenchE_sections, fetched_monkeyE
    print("Checking section of", random_location)

    #Iterate over the trench sections
    for section in trenchE_sections:
        section_id, start_y, end_y = section
        print("Checking section", section_id, "from", start_y, "to", end_y)

        #Check if the random location is within the section
        if end_y <= random_location <= start_y:
            print("Monkey is in section", section_id)

            #Remove the section from the list
            trenchE_sections.remove(section)
            print("Sections left", trenchE_sections[0])

            #Call for delay
            create_delay_tread()
            return section_id
        

#Delay for sending the monkeys 1 second apart
def create_delay():

    for i in range(9):

        #Call for sending the monkey
        send_monkey()
        time.sleep(1)


#Send one monkey to random section        
def send_monkey():
    global trenchE_sections, monkey_locati
    
    #Choose section
    random_section = random.choice(trenchE_sections)
    section_id, start_y, end_y = random_section

    #Call for moving monkey
    move_monkey_threadE(Ae[0]-1, start_y)

    #Remove the section from the list
    trenchE_sections.remove(random_section)
    time.sleep(1)


#Same for Kernesti        
def divide_trenchK():
    global trenchK_sections
    start_y = 400
    section_height = 20

    for i in range(10):
        end_y = start_y - section_height + 1
        section_id = i + 1
        trenchK_sections.append((section_id, start_y, end_y))
        start_y -= section_height

    print(trenchK_sections)
    send_first_monkey_of_tenK()

def send_first_monkey_of_tenK():
    global trenchK, trenchK_sections, monkey_locations
    random_location=random.randint(200, 400)
    move_monkey_threadK(Ak[0]-1, random_location)
    create_small_delay_treadK(random_location)

def create_small_delayK(random_location):
    time.sleep(3)
    check_wich_sectionK(random_location)

def check_wich_sectionK(random_location):
    global trenchK_sections, fetched_monkeyK
    print("Checking section of", random_location)
    for section in trenchK_sections:
        section_id, start_y, end_y = section
        print("Checking section", section_id, "from", start_y, "to", end_y)
        if end_y <= random_location <= start_y:
            print("Monkey is in section", section_id)
            trenchK_sections.remove(section)
            print("Sections left", trenchK_sections[0])
            create_delay_treadK()
            return section_id
    
def create_delayK():
    for i in range(9):
        send_monkeyK()
        time.sleep(1)        
        
def send_monkeyK():
    global trenchK_sections, monkey_locations
    
    
    random_section = random.choice(trenchK_sections)
    section_id, start_y, end_y = random_section

    random_location = random.randint(end_y, start_y)
    move_monkey_threadK(Ak[0]-1, start_y)

    trenchK_sections.remove(random_section)
    time.sleep(1)

#Start the digging this is where the problems start
def start_the_digging():

    #Iterate over the monkeys
    for monkey in monkey_locations:
        monkey = monkey_locations[monkey]
        y_coord = monkey[2]
        x_coord = monkey[1]

        #Get the cell of the trench
        cell=check_trench_cell(y_coord)

        #Start the digging thread
        dig_delay_thread(cell,x_coord, monkey)
    
def dig_delay_thread(cell, x_coord, monkey):
    threading.Thread(target=dig_delay, args=(cell, x_coord, monkey)).start()
    #dig_delay(cell, x_coord, monkey) #tried with single thred, no help

def dig_delay(cell, x_coord, monkey):
    time.sleep(1)
    dig(cell, x_coord, monkey) 

#Digging function
def dig(cell,x_coord, monkey_id):
    global trencE, trenchK

    #delay = 2
    current_cell = cell

    #Check if the monkey is in the trench
    if current_cell is not None and current_cell <= len(trenchE):

        #Iterate over the trench cells left
        for i in range(100-current_cell):
            if x_coord < 500:
                trenchE[current_cell] -= 1
            else:
                trenchK[current_cell] -= 1
                plot_matrices()
                
     
        #Move the monkey to the next cell
        move_monkey_to_next_cell(monkey_id)
        current_cell -= 1

        time.sleep(1)
        #delay *=2

    else:
        return

#Move monkey up one cell
def move_monkey_to_next_cell(monkey_id):
    monkey_id_here, x, y = monkey_id
    print("Moving monkey to next cell", monkey_id, x, y)
    canvas.move(monkey_id, 0, -2)
    canvas.update()
    


###THREADS###
def ernesti_whistle():
    threading.Thread(target=playsound.playsound(whistleE)).start()

def kernesti_whistle():
    threading.Thread(target=playsound.playsound(whistleK)).start()
    
def move_monkey_threadE(target_x, target_y):
    threading.Thread(target=move_monkeyE, args=(target_x, target_y)).start()

def move_monkey_threadK(target_x, target_y):
    threading.Thread(target=move_monkeyK, args=(target_x, target_y)).start()

def monkey_dig_threadE():
    threading.Thread(target=monkey_digE).start()

def monkey_dig_threadK():
    threading.Thread(target=monkey_digK).start()

def play_dig_sound():
    threading.Thread(target=playsound.playsound(digsound)).start()

def fetch_assistant_monkey_threadE():
    threading.Thread(target=fetch_assistant_monkeyE).start()

def create_delay_tread():
    threading.Thread(target=create_delay).start()

def create_delay_treadK():
    threading.Thread(target=create_delayK).start()

def create_small_delay_tread(random_location):
    threading.Thread(target=create_small_delay, args=(random_location,)).start()

def create_small_delay_treadK(random_location):
    threading.Thread(target=create_small_delayK, args=(random_location,)).start()



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
button7 = tk.Button(window, text="Reset", command=reset)
button7.place(x=920, y=10)
button8 = tk.Button(window, text="Assign 10 monkeys E", command=divide_trenchE)
button8.place(x=827, y=40)
button9 = tk.Button(window, text="Assign 10 monkeys K", command=divide_trenchK)
button9.place(x=827, y=70)
button = tk.Button(window, text="START DIGGING", command=start_the_digging)
button.place(x=500, y=100)

window.mainloop()