import tkinter as tk
from PIL import ImageTk, Image
import sys
import os

# Setup tkinter
window = tk.Tk()
window.title("Rebound Predictor Tool")

# Include all code from shotLocation.py
def runSimulation():
    print("TEST")

# Icon
window.iconbitmap('./assets/hockey.ico')


# Display image
rink = tk.PhotoImage(file="./assets/HockeyRinkZone.png")
labelRink = tk.Label(image=rink)
labelRink.pack()

# Set up button(s)
label = tk.Button(window, text = "No functionality here yet", command=runSimulation()).pack()

# Define globals
puckLocationX = 0
puckLocationY = 0
puckPlaced = False

# Display x-y of mouse
# Will use this to detect where puck is placed
def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))

# Show puck on interface at desired position
def onClick(event):
    global puckLocationX, puckLocationY
    print ("Clicked at", event.x, event.y)
    puckLocationX, puckLocationY = event.x, event.y

    load = Image.open("./assets/puck.png")
    render = ImageTk.PhotoImage(load)
    img = tk.Label(window, image=render)
    img.image = render
    img.place(x=puckLocationX-10, y=puckLocationY-10)
    puckPlaced = True


def checkKeyPress(event):
    print ("Pressed", repr(event.char))
    if (event.char == 'q'):
        restart()
    elif (event.char == '\r'):
        runSimulation()
    else:
        print(puckLocationX, puckLocationY)

def restart():
    print("TEST")
    os.execl(sys.executable, sys.executable, *sys.argv)


window.bind('<Motion>', motion)
window.bind('<Button-2>', onClick)
window.bind("<Key>", checkKeyPress)

window.geometry("+600+300")

window.mainloop()
