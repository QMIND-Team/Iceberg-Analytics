import csv, random
import pandas as pd

data = []


def importData():
    global data
    data = pd.read_csv("data/output.csv")


def processData():
    global data
    i = 0
    for i in range(0, data.shape[0]):
        x = data.iloc[i, 8]
        y = data.iloc[i, 9]
        if x < 0:
            x = -x
            y = -y
        if y > 690:
            if 2650 >= x > 2050:
                data.iloc[i, 14] = "A1"
            elif 2050 >= x > 1400:
                data.iloc[i, 14] = "A2"
            elif 1400 >= x >= 750:
                data.iloc[i, 14] = "A3"
            else:
                data.iloc[i, 14] = "BAD"
        elif 690 >= y > 0:
            if 2650 >= x > 2050:
                data.iloc[i, 14] = "B1"
            elif 2050 >= x > 1400:
                data.iloc[i, 14] = "B2"
            elif 1400 >= x >= 750:
                data.iloc[i, 14] = "B3"
            else:
                data.iloc[i, 14] = "BAD"
        elif 0 >= y > -690:
            if 2650 >= x > 2050:
                data.iloc[i, 14] = "C1"
            elif 2050 >= x > 1400:
                data.iloc[i, 14] = "C2"
            elif 1400 >= x >= 750:
                data.iloc[i, 14] = "C3"
            else:
                data.iloc[i, 14] = "BAD"
        else:
            if 2650 >= x > 2050:
                data.iloc[i, 14] = "D1"
            elif 2050 >= x > 1400:
                data.iloc[i, 14] = "D2"
            elif 1400 >= x >= 750:
                data.iloc[i, 14] = "D3"
            else:
                data.iloc[i, 14] = "BAD"
    print(data["Shot location"])


importData()
processData()
