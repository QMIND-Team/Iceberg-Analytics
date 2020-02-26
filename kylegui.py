from tkinter import *
from PIL import Image, ImageTk
from predictor import singlePredict, startup

global puckX, puckY, goalieX, goalieY, model
model = startup()

puckX = -1
puckY = -1
goalieX = -1
goalieY = -1
def click(event):
     global puckX, puckY, goalieX, goalieY, model
     if(str(event.widget) == '.!label'):
        img.place(x=event.x-10, y=event.y)
        puckX, puckY = event.x, event.y
     elif(str(event.widget) == '.!label2'):
        img2.place(x=event.x+650, y=event.y-10)
        goalieX, goalieY = event.x, event.y
     elif(str(event.widget) == '.!button'):
         if goalieX <= 440 and goalieX >= 60 and goalieY <= 440 and goalieY >= 100:
            if puckY >= 100 and puckY <= 490:
               print("The puck is at: "+str(puckX)+", "+str(puckY)+"\n and the goalie coords are: "+str(goalieX)+", "+str(goalieY))
               iceBin, shotBin = convert(goalieX, goalieY, puckX, puckY)
               bins = singlePredict(model, iceBin,shotBin)
               for i in range(len(bins)):
                  print ('Bin' , i , ' --- ', bins[i])

            else:
               print("Invalid input. Please make sure the puck is in a shooting position.")
         else:
            print("Invalid input. Please make sure the target is in the net.")
        #would implement calling the shotLocation file here but need to check if inputs are legal first

     var.set("Puck Coordinates: "+str(puckX)+', '+str(puckY)+"\nGoalie Coordinates: "+str(goalieX)+', '+str(goalieY))

def convert(gX, gY, pX, pY):
   return 1,1


window = Tk()
window.title("Rebound Predictor Tool")
photo1 = PhotoImage(file="assets/rink.png")
Label (window, image=photo1, bg="blue") .grid(row=0, column=0, sticky=W)
v = Image.open("assets/net.png").resize((500, 500), Image.ANTIALIAS)
photo2 = ImageTk.PhotoImage(v)
Label (window, image=photo2, bg="blue") .grid(row=0, column=1, sticky=W)

b = Button (window, text="Check Rebound", width = 13) .grid(row=1, column =1, sticky=W)

load = Image.open("./assets/puck.png")
render = ImageTk.PhotoImage(load)
img = Label(window, image = render)

load2 = Image.open("./assets/target.png")
render2 = ImageTk.PhotoImage(load2)
img2 = Label(window, image = render2, bg = 'black')

var = StringVar()

msg = Message(window, textvariable = var, width = 200, relief = RAISED) .grid(row=1, column=0)

window.bind('<Button-1>', click)
window.mainloop()