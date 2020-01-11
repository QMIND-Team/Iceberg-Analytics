import csv, random, math
import numpy as np
import pandas as pd

import tensorflow as tf

from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

data = []


# read data from csv
def importData():
    global data
    data = pd.read_csv("data/output.csv")


# calculate output angle
def angleCalc(x, y):
    if y == 0:
        y = 0.0001
    if x == 2650:
        x = 2650.0001
    if y > 0:
        return 45 - math.degrees(math.atan((x - 2650) / y))
    elif x < 0:
        return 135 + math.degrees(math.atan(y / (x - 2650)))
    else:
        return 225 - math.degrees(math.atan((x - 2650) / y))


def processData():
    global data
    toDelete = [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 15]
    # 0 = Game id
    # 1 = Home team name
    # 2 = Away team name
    # 3 = Event id
    # 4 = Abs time
    # 5 = Event
    # 6 = Shooter team status
    # 7 = Shooter name
    # 8 = Shot x
    # 9 = Shot y
    # 10 = Goalie team status
    # 11 = Goalie name
    # 12 = Goalie x
    # 13 = Goalie y
    # 14 = Shot location
    # 15 = Shot category
    # 16 = Save type
    # 17 = Rebound
    # 18 = Rebound x
    # 19 = Rebound y
    # Current data: Shot X , Shot Y, ShotLocation, Rebound (T/F), ReboundX, Rebound Y
    data = data.drop(data.columns[toDelete], axis=1)
    i = 0
    angles = []
    angleBins = []
    for i in range(0, data.shape[0]):
        x = data.iloc[i, 0]
        y = data.iloc[i, 1]
        xAngle = data.iloc[i, 5]
        yAngle = data.iloc[i, 6]
        # flip data for right side of net
        if x < 0:
            x = -x
            y = -y
            xAngle = -xAngle
            yAngle = -yAngle
            data.iloc[i, 0] = x
            data.iloc[i, 1] = y
            # calculate angle
        newAngle = angleCalc(xAngle, yAngle)
        angles.append(newAngle)
        if math.isnan(newAngle):
            if isinstance(data.iloc[i, 3], str):
                # -1 = NO REBOUND - SAVE
                angleBins.append(-1)
            else:
                # -1 = NO REBOUND - GOAL
                 angleBins.append(-2)
                 data.iloc[i,3] = "GOAL"
        else:
            angleBins.append(int(newAngle / 15))
        # calculate shooting bin
        if y > 690:
            if 2650 >= x > 2050:
                data.iloc[i, 2] = 1
            elif 2050 >= x > 1400:
                data.iloc[i, 2] = 2
            elif 1400 >= x >= 750:
                data.iloc[i, 2] = 3
            else:
                data.iloc[i, 2] = -999
        elif 690 >= y > 0:
            if 2650 >= x > 2050:
                data.iloc[i, 2] = 4
            elif 2050 >= x > 1400:
                data.iloc[i, 2] = 5
            elif 1400 >= x >= 750:
                data.iloc[i, 2] = 6
            else:
                data.iloc[i, 2] = -999
        elif 0 >= y > -690:
            if 2650 >= x > 2050:
                data.iloc[i, 2] = 7
            elif 2050 >= x > 1400:
                data.iloc[i, 2] = 8
            elif 1400 >= x >= 750:
                data.iloc[i, 2] = 9
            else:
                data.iloc[i, 2] = -999
        else:
            if 2650 >= x > 2050:
                data.iloc[i, 2] = 10
            elif 2050 >= x > 1400:
                data.iloc[i, 2] = 11
            elif 1400 >= x >= 750:
                data.iloc[i, 2] = 12
            else:
                data.iloc[i, 2] = -999
    #print(data["Shot location"])
    # add new angles column
    data.insert(7, "Rebound_Angle", angles, True)
    data.insert(8, "Rebound_Bin", angleBins, True)

def analyzeData():
    global data
    toDelete = [0,1,3,4,5,6,7]
    data = data.drop(data.columns[toDelete], axis=1)
    train,test = train_test_split(data, test_size = 0.2)
    train,val = train_test_split(data, test_size = 0.2)
    batch_size = 32
    train_ds = df_to_dataset(train, batch_size = batch_size)
    test_ds = df_to_dataset(test, shuffle = False, batch_size = batch_size)
    val_ds = df_to_dataset(val, shuffle = False, batch_size = batch_size)

    feature_columns = []

    feature_columns.append(feature_column.numeric_column('Shot_location'))

    feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

    model = tf.keras.Sequential([
        feature_layer,
        layers.Dense(128, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])

    model.fit(train_ds,
            validation_data=val_ds,
            epochs=5)

    loss,accuracy = model.evaluate(test_ds)



def df_to_dataset(dataframe, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop("Rebound_Bin")
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size = len(dataframe))
    ds = ds.batch(batch_size)
    return ds


importData()
processData()
analyzeData()
