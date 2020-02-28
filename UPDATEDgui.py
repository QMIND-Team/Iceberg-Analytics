from tkinter import *
from PIL import Image, ImageTk
from predictor import singlePredict, startup
from blank import getNums
import math

#TO DO: LOOK AT THE STUFF AROUND FIND COORDINATES, FIND OUT WHERE GOAL/STOPPAGE PERCENTAGES DISPLAY

'''
COORDINATES (x,y FROM 0,0 @ top left)
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
#build model in predictor and load
model = startup()
#initialize values
puckX = -1
puckY = -1
goalieX = -1
goalieY = -1
#window width, window height, triangle length... 1540 x 830 for fullscreen
WW = 1100
WH = 700
tri = 100
#on click
def click(event):
   global puckX, puckY, goalieX, goalieY, model
   #find where click occured
   action = findZone(event.x, event.y)
   #click occurs on the ice (left)
   if (action == "ice"):
      img.place(x=event.x-10, y=event.y-10)
      puckX, puckY = event.x, event.y
   #click occurs on the net (right)
   elif (action == "net"):
      img2.place(x=event.x-10, y=event.y-10)
      goalieX, goalieY = event.x, event.y
      resetGoalieShapes(goalieX, goalieY)
   #click occurs on submit button
   elif (action == "submit"):
      #make sure target is aimed at not
      if goalieX >= 670*WW/1100 and goalieX <= 1020*WW/1100 and goalieY >= 180*WH/700 and goalieY <= 550*WH/700:
         #make sure puck is in shooting position
         if puckX >= 0*WW/1100 and puckX <= 600*WW/1100 and puckY >= 190*WH/700 and puckY <= 600*WH/700:
            #convert to get the bins
            iceBin, shotBin = convert(goalieX, goalieY, puckX, puckY)
            #get prediction/percentages
            bins = singlePredict(model, iceBin,shotBin)
            #set new shapes/output colors
            resetAngleShapes(bins)
            w.itemconfig(e1, text = "")
            w.itemconfig(e1, text = "")
         else:
            #error messages
            w.itemconfig(e0, text = "Error: make sure puck location is valid.")
            w.itemconfig(e1, text = "")
      else:
         #error messages
         w.itemconfig(e1, text = "Error: make sure target is valid.")
         w.itemconfig(e0, text = "")

#find where click occured
def findZone(x,y):
   rVal = "none"
   #in submit button
   if (x >= 500*WW/1100 and x <= 600*WW/1100 and y >= 630*WH/700 and y <= 670*WH/700):
      rVal =  "submit"
   #in ice
   elif (x >= 0*WW/1100 and x <= 600*WW/1100 and y >= 100*WH/700 and y <= 600*WH/700):
      rVal =  "ice"
   #in net
   elif (x >= 620*WW/1100 and x <= 1070*WW/1100 and y >= 100*WH/700 and y <= 600*WH/700):
      rVal = "net"
   return rVal

#color shapes , change text
def resetAngleShapes(nums):
   colors = []
   percents = []
   for i in range(9):
      #CHANGE THESE NUMBERS TO WHATEVER RANGE WE DECIDE
      if nums[i] <= 0.1:
         temp = "red"
      elif nums[i] > 0.1 and nums [i] <= 0.2:
         temp = "blue"
      elif nums[i] > 0.2 and nums [i] <= 0.3:
         temp = "yellow"
      else:
         temp = "green"
      colors.append(temp)
      tstring = str(nums[i]*100)+'%'
      percents.append(tstring)
   #change colors
   w.itemconfig(t0, fill = colors[0])
   w.itemconfig(t1, fill = colors[1])
   w.itemconfig(t2, fill = colors[2])
   w.itemconfig(t3, fill = colors[3])
   w.itemconfig(t4, fill = colors[4])
   w.itemconfig(t5, fill = colors[5])
   w.itemconfig(t6, fill = colors[6])
   w.itemconfig(t7, fill = colors[7])
   w.itemconfig(t8, fill = colors[8])
   #change texts to new percentages
   w.itemconfig(p0, text = percents[0][:5])
   w.itemconfig(p1, text = percents[1][:5])
   w.itemconfig(p2, text = percents[2][:5])
   w.itemconfig(p3, text = percents[3][:5])
   w.itemconfig(p4, text = percents[4][:5])
   w.itemconfig(p5, text = percents[5][:5])
   w.itemconfig(p6, text = percents[6][:5])
   w.itemconfig(p7, text = percents[7][:5])
   w.itemconfig(p8, text = percents[8][:5])

#reset goalie colors, change green to wherever clicked
def resetGoalieShapes(x,y):
   w.itemconfig(g0, fill = 'red')
   w.itemconfig(g1, fill = 'red')
   w.itemconfig(g2, fill = 'red')
   w.itemconfig(g3, fill = 'red')
   w.itemconfig(g4, fill = 'red')
   #find where click occured
   if (x >= 775*WW/1100 and x <=900*WW/1100 and y >= 180*WH/700 and y <= 550*WH/700):
      w.itemconfig(g2, fill = 'green')  
   elif (x < 775*WW/1100 and x >= 670*WW/1100 and y <=340*WH/700 and y >= 180*WH/700):
      w.itemconfig(g0, fill = 'green') 
   elif (x < 775*WW/1100 and x > 670*WW/1100 and y >340*WH/700 and y <=550*WH/700):
      w.itemconfig(g1, fill = 'green') 
   elif (x > 900*WW/1100 and x <=1020*WW/1100 and y <=340*WH/700 and y >= 180*WH/700):
      w.itemconfig(g3, fill = 'green') 
   elif (x > 900*WW/1100 and x <= 1020*WW/1100 and y >340*WH/700 and y <= 550*WH/700):
      w.itemconfig(g4, fill = 'green') 


#Have to convert all these to shot locations on new surface, probably different
#Also look at the glove/blocker/stick stuff
def convert(gx, gy, pX, pY):
   #GET LOCATION ON ICE
   #Y--blueline
   if pY > 320:
      #left
      if pX < 165:
         sL = 12
      #left middle
      elif 165 <= pX < 300:
         sL = 9
      #right middle
      elif 300 <= pX < 450:
         sL = 6
      #right
      else: 
         sL = 3
   #Y-- middle
   elif 230 >= pY > 126:
      #left
      if pX < 165:
         sL =11
      #left middle
      elif 165 <= pX < 300:
         sL = 8
      #right middle
      elif 300 <= pX < 450:
         sL = 5
      #right
      else:
         sL = 2
   #Y -- net
   elif  126 >= pY > 0:
      #left
      if pX < 165:
         sL = 10
      #left middle
      elif 165 <= pX < 300:
         sL = 7
      #right middle
      elif 300 <= pX < 450:
         sL = 4
      #right
      else:
         sL = 1
   else:
      sL = 13

   #GET LOCATION ON GOALIE (TARGET)
   if (gx >= 775*WW/1100 and gx <=900*WW/1100 and gy >= 180*WH/700 and gy <= 550*WH/700):
      gOutput = 4
   elif (gx < 775*WW/1100 and gx >= 670*WW/1100 and gy <=340*WH/700 and gy >= 180*WH/700):
      gOutput = 1
   elif (gx < 775*WW/1100 and gx > 670*WW/1100 and gy >340*WH/700 and gy <=550*WH/700):
      gOutput = 2
   elif (gx > 900*WW/1100 and gx <=1020*WW/1100 and gy <=340*WH/700 and gy >= 180*WH/700):
      gOutput = 0
   elif (gx > 900*WW/1100 and gx <= 1020*WW/1100 and gy >340*WH/700 and gy <= 550*WH/700):
      gOutput = 3
   return sL,gOutput


window = Tk()
window.title("Rebound Predictor Tool")

#Main Body: two side by side images
w = Canvas(window, width=WW, height=WH)
#Overall background
w.create_rectangle(0*WW/1100,0*WH/700,1100*WW/1100,700*WH/700, fill = "white")
#Separating Lines
w.create_line(0*WW/1100,605*WH/700,1100*WW/1100,605*WH/700, width = 3)
w.create_line(0*WW/1100,98*WH/700,1100*WW/1100,98*WH/700, width = 3)
w.create_line(610*WW/1100, 100*WH/700, 610*WW/1100, 605*WH/700, width = 3)
#Header Text
w.create_text(580*WW/1100,20*WH/700, font=("Purisa", 20) ,text = "Hockey Shot Rebound Predictor")
w.create_text(300*WW/1100,80*WH/700, font=("Purisa", 15) ,text = "Location On Ice")
w.create_text(850*WW/1100,80*WH/700, font=("Purisa", 15) ,text = "Location On Goaltender")
#Image creation
w.grid(row = 0, column = 0) 
i1 = ImageTk.PhotoImage(Image.open("assets/HockeyRinkZone.png").resize((int(600*WW/1100), int(500*WH/700))))
w.create_image(0*WW/1100, 100*WH/700, anchor = NW, image = i1)
i2 = ImageTk.PhotoImage(Image.open("assets/startingGoalieImage.png").resize((int(450*WW/1100), int(500*WH/700))))
w.create_image(620*WW/1100, 100*WH/700, anchor = NW, image = i2)
#left click
w.bind("<Button-1>", click)
#Button to call predictor function
w.create_rectangle (500*WW/1100,630*WH/700,600*WW/1100, 670*WH/700, fill = "#98FB98")
w.create_text(550*WW/1100,650*WH/700, text = "PREDICT")
#OUTPUT TRIANGLES
startX = 300*WW/1100
startY = 195*WH/700
tri = tri*WW/1100
#START THESE FILLS ALL OFF AS fill = ""
t0 = w.create_polygon(startX,startY,tri*math.cos(math.radians(-45))+startX,tri*math.sin(math.radians(-45))+startY,tri*math.cos(math.radians(-15))+startX,tri*math.sin(math.radians(-15))+startY,fill = "")
t1 = w.create_polygon(startX,startY,tri*math.cos(math.radians(-15))+startX,tri*math.sin(math.radians(-15))+startY,tri*math.cos(math.radians(15))+startX,tri*math.sin(math.radians(15))+startY,fill = "", stipple = "gray50")
t2 = w.create_polygon(startX,startY,tri*math.cos(math.radians(15))+startX,tri*math.sin(math.radians(15))+startY,tri*math.cos(math.radians(45))+startX,tri*math.sin(math.radians(45))+startY,fill = "")
t3 = w.create_polygon(startX,startY,tri*math.cos(math.radians(45))+startX,tri*math.sin(math.radians(45))+startY,tri*math.cos(math.radians(75))+startX,tri*math.sin(math.radians(75))+startY,fill = "")
t4 = w.create_polygon(startX,startY,tri*math.cos(math.radians(75))+startX,tri*math.sin(math.radians(75))+startY,tri*math.cos(math.radians(105))+startX,tri*math.sin(math.radians(105))+startY,fill = "")
t5 = w.create_polygon(startX,startY,tri*math.cos(math.radians(105))+startX,tri*math.sin(math.radians(105))+startY,tri*math.cos(math.radians(135))+startX,tri*math.sin(math.radians(135))+startY,fill = "")
t6 = w.create_polygon(startX,startY,tri*math.cos(math.radians(135))+startX,tri*math.sin(math.radians(135))+startY,tri*math.cos(math.radians(165))+startX,tri*math.sin(math.radians(165))+startY,fill = "")
t7 = w.create_polygon(startX,startY,tri*math.cos(math.radians(165))+startX,tri*math.sin(math.radians(165))+startY,tri*math.cos(math.radians(195))+startX,tri*math.sin(math.radians(195))+startY,fill = "")
t8 = w.create_polygon(startX,startY,tri*math.cos(math.radians(195))+startX,tri*math.sin(math.radians(195))+startY,tri*math.cos(math.radians(225))+startX,tri*math.sin(math.radians(225))+startY,fill = "")

#OUTPUT PERCENTAGES
p0 = w.create_text(363*WW/1100, 157*WH/700, text = "")
p1 = w.create_text(373*WW/1100, 193*WH/700, text = "")
p2 = w.create_text(360*WW/1100, 228*WH/700, text = "")
p3 = w.create_text(335*WW/1100, 255*WH/700, text = "")
p4 = w.create_text(300*WW/1100, 264*WH/700, text = "")
p5 = w.create_text(265*WW/1100, 255*WH/700, text = "")
p6 = w.create_text(240*WW/1100, 228*WH/700, text = "")
p7 = w.create_text(227*WW/1100, 193*WH/700, text = "")
p8 = w.create_text(237*WW/1100, 157*WH/700, text = "")

#GOALIE SHAPES
g0 = w.create_rectangle(675*WW/1100,160*WH/700,775*WW/1100, 340*WH/700, fill = 'red', stipple = 'gray50')
g1 = w.create_rectangle(675*WW/1100,340*WH/700,775*WW/1100, 550*WH/700, fill = 'red' ,stipple = 'gray50')
g2 = w.create_rectangle(775*WW/1100,160*WH/700,900*WW/1100, 550*WH/700, fill = 'red' ,stipple = 'gray50')
g3 = w.create_rectangle(900*WW/1100,160*WH/700,1015*WW/1100,340*WH/700, fill = 'red',stipple = 'gray50')
g4 = w.create_rectangle(900*WW/1100,340*WH/700,1015*WW/1100, 550*WH/700, fill = 'red' ,stipple = 'gray50')

#ErrorMessages
e0 = w.create_text(225*WW/1100,650*WH/700, text = "")
e1 = w.create_text(875*WW/1100,650*WH/700, text = "")

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

mainloop()
