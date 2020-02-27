from tkinter import *
from PIL import Image, ImageTk
#from predictor import singlePredict, startup
from blank import getNums
import math

'''
COORDINATES (x,y FROM top left)
Rink: (000,000) - (600,000)
          |           |
      (000,500) - (600,500)

Net:  (620,000) - (1070,000)
         |           |
      (620,500) - (1070,500)

Sub:  (500,530) - (600,530)
         |           |
      (500,570) - (600,570)



'''

global puckX, puckY, goalieX, goalieY, model, WW, WH, tri
#model = startup()

puckX = -1
puckY = -1
goalieX = -1
goalieY = -1

#CURRENTLY HARDCODED --- to change, set all x values to VAL*WW/1100, all y values to VAL/WH/700
WW = 1100
WH = 700
tri = 100

def click(event):
   global puckX, puckY, goalieX, goalieY, model
   action = findZone(event.x, event.y)
   print(event.x, event.y, action)
   if (action == "ice"):
      img.place(x=event.x-10, y=event.y-10)
      puckX, puckY = event.x, event.y
   elif (action == "net"):
      img2.place(x=event.x-10, y=event.y-10)
      goalieX, goalieY = event.x, event.y
   elif (action == "submit"):
      if goalieX >= 670 and goalieX <= 1020 and goalieY >= 180 and goalieY <= 550:
         if puckX >= 0 and puckX <= 600 and puckY >= 190 and puckY <= 600:
            print("The puck is at: "+str(puckX)+", "+str(puckY)+"\n and the goalie coords are: "+str(goalieX)+", "+str(goalieY))
            iceBin, shotBin = convert(goalieX, goalieY, puckX, puckY)
            bins = getNums()
            #bins = singlePredict(model, iceBin,shotBin)
            for i in range(len(bins)):
               print ('Bin' , i , ' --- ', bins[i])

         else:
            print("Invalid input. Please make sure the puck is in a shooting position.")
      else:
         print("Invalid input. Please make sure the target is in the net.")
   #would implement calling the shotLocation file here but need to check if inputs are legal first

def findZone(x,y):
   rVal = "none"
   #in submit button
   if (x >= 500 and x <= 600 and y >= 630 and y <= 670):
      rVal =  "submit"
   #in ice
   elif (x >= 0 and x <= 600 and y >= 100 and y <= 600):
      rVal =  "ice"
   #in net
   elif (x >= 620 and x <= 1070 and y >= 100 and y <= 600):
      rVal = "net"
   return rVal

def convert(gX, gY, pX, pY):
   if pY > 252:
      if 165 >= pX > 0:
         sL = 12
      elif 330 >= pX > 165:
         sL = 9
      elif 495 >= pX >= 330:
         sL = 6
      else:
         sL = 3
   elif 230 >= pY > 126:
      if 165 >= pX > 0:
         sL = 11
      elif 330 >= pX > 165:
         sL = 8
      elif 495 >= pX >= 330:
         sL = 5
      else:
         sL = 2
   elif  126 >= pY > 0:
      if 165 >= pX > 0:
         sL = 10
      elif 330 >= pX > 165:
         sL = 7
      elif 495 >= pX >= 330:
         sL = 4
      else:
         sL = 1
   else:
      sL = 13
   return sL,1


window = Tk()
window.title("Rebound Predictor Tool")

#Main Body: two side by side images
w = Canvas(window, width=1100, height=700)
#Overall background
w.create_rectangle(0,0,1100,700, fill = "white")
#Separating Lines
w.create_line(0,605,1100,605, width = 3)
w.create_line(0,98,1100,98, width = 3)
w.create_line(610, 100, 610, 605, width = 3)
#Header Text
w.create_text(580,20, font=("Purisa", 20) ,text = "Hockey Shot Rebound Predictor")
w.create_text(300,80, font=("Purisa", 15) ,text = "Location On Ice")
w.create_text(850,80, font=("Purisa", 15) ,text = "Location On Goaltender")
#Image creation
w.grid(row = 0, column = 0) 
i1 = ImageTk.PhotoImage(Image.open("assets/rink.png").resize((600, 500)))
w.create_image(0, 100, anchor = NW, image = i1)
i2 = ImageTk.PhotoImage(Image.open("assets/net.png").resize((450, 500)))
w.create_image(620, 100, anchor = NW, image = i2)
#left click
w.bind("<Button-1>", click)
#Button to call predictor function
w.create_rectangle (500,630,600, 670, fill = "#98FB98")
w.create_text(550,650, text = "PREDICT")
#OUTPUT TRIANGLES
startX = 300
startY = 195
w.create_polygon(startX,startY,tri*math.cos(math.radians(-45))+startX,tri*math.sin(math.radians(-45))+startY,tri*math.cos(math.radians(-15))+startX,tri*math.sin(math.radians(-15))+startY,fill = "red")
w.create_polygon(startX,startY,tri*math.cos(math.radians(-15))+startX,tri*math.sin(math.radians(-15))+startY,tri*math.cos(math.radians(15))+startX,tri*math.sin(math.radians(15))+startY,fill = "blue")
w.create_polygon(startX,startY,tri*math.cos(math.radians(15))+startX,tri*math.sin(math.radians(15))+startY,tri*math.cos(math.radians(45))+startX,tri*math.sin(math.radians(45))+startY,fill = "red")
w.create_polygon(startX,startY,tri*math.cos(math.radians(45))+startX,tri*math.sin(math.radians(45))+startY,tri*math.cos(math.radians(75))+startX,tri*math.sin(math.radians(75))+startY,fill = "blue")
w.create_polygon(startX,startY,tri*math.cos(math.radians(75))+startX,tri*math.sin(math.radians(75))+startY,tri*math.cos(math.radians(105))+startX,tri*math.sin(math.radians(105))+startY,fill = "red")
w.create_polygon(startX,startY,tri*math.cos(math.radians(105))+startX,tri*math.sin(math.radians(105))+startY,tri*math.cos(math.radians(135))+startX,tri*math.sin(math.radians(135))+startY,fill = "blue")
w.create_polygon(startX,startY,tri*math.cos(math.radians(135))+startX,tri*math.sin(math.radians(135))+startY,tri*math.cos(math.radians(165))+startX,tri*math.sin(math.radians(165))+startY,fill = "red")
w.create_polygon(startX,startY,tri*math.cos(math.radians(165))+startX,tri*math.sin(math.radians(165))+startY,tri*math.cos(math.radians(195))+startX,tri*math.sin(math.radians(195))+startY,fill = "blue")
w.create_polygon(startX,startY,tri*math.cos(math.radians(195))+startX,tri*math.sin(math.radians(195))+startY,tri*math.cos(math.radians(225))+startX,tri*math.sin(math.radians(225))+startY,fill = "red")


#Import images
#load puck
load = Image.open("./assets/puck.png")
render = ImageTk.PhotoImage(load)
img = Label(window, image = render)
#load target
load2 = Image.open("./assets/target.png")
render2 = ImageTk.PhotoImage(load2)
img2 = Label(window, image = render2, bg = 'black')

# Icon
window.iconbitmap('./assets/hockey.ico')

window.bind('<Button-1>', click)
window.mainloop()
