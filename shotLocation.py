import csv, random, math
import pandas as pd

data = []


def importData():
    global data
    data = pd.read_csv("data/output.csv")

def anglecalc(x,y):
    if y == 0:
        y = 0.0001
    if x == -2650:
        x = -2650.0001
    if y>0:
        return (45 + math.degrees(math.atan((x+2650)/y)))
    elif (x+2650)>0:
        return (135 - math.degrees(math.atan(y/(x+2650))))
    else:
        return (225 + math.degrees(math.atan((x+2650)/y)))

def processData():
    global data
    toDelete = [0,1,2,3,4,5,6,7,10,11,12,13,15,16]
    #Shot X , Shot Y, ShotLocation, Rebound (T/F), ReboundX, Rebound Y
    data = data.drop(data.columns[toDelete], axis=1)
    i = 0
    angles = []
    for i in range(0, data.shape[0]):
        x = data.iloc[i, 0]
        y = data.iloc[i, 1]
        xAngle = data.iloc[i,4]
        yAngle = data.iloc[i,5]
        newAngle = anglecalc(xAngle, yAngle)
        angles.append(newAngle)
        if x < 0:
            x = -x
            y = -y
            data.iloc[i, 0] = x
            data.iloc[i, 1] = y
        if y > 690:
            if 2650 >= x > 2050:
                data.iloc[i, 2] = "A1"
            elif 2050 >= x > 1400:
                data.iloc[i, 2] = "A2"
            elif 1400 >= x >= 750:
                data.iloc[i, 2] = "A3"
            else:
                data.iloc[i, 2] = "BAD"
        elif 690 >= y > 0:
            if 2650 >= x > 2050:
                data.iloc[i, 2] = "B1"
            elif 2050 >= x > 1400:
                data.iloc[i, 2] = "B2"
            elif 1400 >= x >= 750:
                data.iloc[i, 2] = "B3"
            else:
                data.iloc[i, 2] = "BAD"
        elif 0 >= y > -690:
            if 2650 >= x > 2050:
                data.iloc[i, 2] = "C1"
            elif 2050 >= x > 1400:
                data.iloc[i, 2] = "C2"
            elif 1400 >= x >= 750:
                data.iloc[i, 2] = "C3"
            else:
                data.iloc[i, 2] = "BAD"
        else:
            if 2650 >= x > 2050:
                data.iloc[i, 2] = "D1"
            elif 2050 >= x > 1400:
                data.iloc[i, 2] = "D2"
            elif 1400 >= x >= 750:
                data.iloc[i, 2] = "D3"
            else:
                data.iloc[i, 2] = "BAD"
    print(data["Shot location"])

    print (len(angles))

    data.insert(6, "Rebound Angle", angles, True)

    print (data["Rebound Angle"])


importData()
processData()
