import tkinter as tk
from PIL import ImageTk, Image
import sys

# Define globals
puckLocationX = 0
puckLocationY = 0
puckPlaced = False

class reboundPredictionApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}

        for page in (StartPage, Simulation):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0)

        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

def example():
    print("TEST")

def displayRink():
    rink = tk.PhotoImage(file="./assets/HockeyRinkZone.png")
    label = tk.Label(image=rink)
    label.image = rink
    label.pack()

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
    img = tk.Label(app, image=render)
    img.image = render
    img.place(x=puckLocationX-8, y=puckLocationY-5)
    puckPlaced = True

def checkPuck(event):
    print ("Pressed", repr(event.char))
    print(puckLocationX, puckLocationY)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        background = tk.PhotoImage(file="./assets/titlePage.png")
        backgroundLabel = tk.Label(image=background)
        backgroundLabel.place(x=0,y=0,relwidth=1,relheight=1)
        backgroundLabel.image = background
        backgroundLabel.pack()

        label1 = tk.Label(self, text="Start Page")
        label1.pack(pady=10,padx=10)

        startButton = tk.Button(self, text="Start Simulation", command=lambda: controller.show_frame(Simulation))
        startButton.pack()

class Simulation(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Predict Rebound")
        label.pack(pady=10,padx=10)

        backButton = tk.Button(self, text="Main Menu", command=lambda: [controller.show_frame(StartPage), displayRink()])
        backButton.pack()

app = reboundPredictionApp()
app.bind('<Motion>', motion)
app.bind('<Button-1>', onClick)
app.bind("<Key>", checkPuck)
app.mainloop()
