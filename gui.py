import tkinter as tk
from tkinter import *

# Setup tkinter
window = tk.Tk()
window.title("Rebound Predictor Tool")
label = tk.Button(window, text = "Rebound tool").pack()

# Display image
image = tk.PhotoImage(file="./assets/HockeyRinkZone.png")
label = tk.Label(image=image)
label.pack()

# Define globals
puckLocationX = 0
puckLocationY = 0

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
    img = Label(self, image=render)
    img.image = render
    img.place(x=puckLocationX, y=puckLocationY)


def checkPuck(event):
    print ("Pressed", repr(event.char))
    print(puckLocationX, puckLocationY)



window.bind('<Motion>', motion)
window.bind('<Button-1>', onClick)
window.bind("<Key>", checkPuck)

window.mainloop()
