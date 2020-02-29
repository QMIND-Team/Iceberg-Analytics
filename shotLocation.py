import csv, random, math
import numpy as np
import pandas as pd

import tensorflow as tf

import sklearn

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
        shotType = data.iloc[i, 3]
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
                angleBins.append(8)
            else:
                # -1 = NO REBOUND - GOAL
                 angleBins.append(9)
                 data.iloc[i,3] = "GOAL"
        else:
            num = (int(newAngle / 30))
            if num >= 8:
                num = 7
            angleBins.append(num)
        # calculate shooting bin
        if y > 690:
            if 2650 >= x > 2050:
                data.iloc[i, 2] = 1
            elif 2050 >= x > 1400:
                data.iloc[i, 2] = 2
            elif 1400 >= x >= 750:
                data.iloc[i, 2] = 3
            else:
                data.iloc[i, 2] = 13
        elif 690 >= y > 0:
            if 2650 >= x > 2050:
                data.iloc[i, 2] = 4
            elif 2050 >= x > 1400:
                data.iloc[i, 2] = 5
            elif 1400 >= x >= 750:
                data.iloc[i, 2] = 6
            else:
                data.iloc[i, 2] = 13
        elif 0 >= y > -690:
            if 2650 >= x > 2050:
                data.iloc[i, 2] = 7
            elif 2050 >= x > 1400:
                data.iloc[i, 2] = 8
            elif 1400 >= x >= 750:
                data.iloc[i, 2] = 9
            else:
                data.iloc[i, 2] = 13
        else:
            if 2650 >= x > 2050:
                data.iloc[i, 2] = 10
            elif 2050 >= x > 1400:
                data.iloc[i, 2] = 11
            elif 1400 >= x >= 750:
                data.iloc[i, 2] = 12
            else:
                data.iloc[i, 2] = 13
    # Convert Save Type to int values
        if shotType == ("SHOT_ATTEMPT_UPPER_LEFT"):
            data.iloc[i, 3] = 0
        elif shotType == ("SHOT_ATTEMPT_TOP_MIDDLE"):
            data.iloc[i, 3] = 1
        elif shotType == ("SHOT_ATTEMPT_UPPER_RIGHT"):
            data.iloc[i, 3] = 2
        elif shotType == ("SHOT_ATTEMPT_LOWER_LEFT"):
            data.iloc[i, 3] = 3
        elif shotType == ("SHOT_ATTEMPT_BOTTOM_MIDDLE"):
            data.iloc[i, 3] = 4
        elif shotType == ("SHOT_ATTEMPT_LOWER_RIGHT"):
            data.iloc[i, 3] = 5
        else:
            data.iloc[i, 3] = 6
    # add new angles column
    data.insert(7, "Rebound_Angle", angles, True)
    data.insert(8, "Rebound_Bin", angleBins, True)
    print (max(angleBins),"MAX")
    print (min(angleBins),"MIN")

def analyzeData():
    global data
    #delete unnecessary cols
    toDelete = [0,1,4,5,6,7]
    newData = data.drop(data.columns[toDelete], axis=1)
    #create new output col, able to manipulate
    newData['RS'] = newData['Rebound_Bin']
    uniques = []
    #check for unique numbers (if there's a hole we'll need to check for this later)
    for i in range (0, newData.shape[0]):
        temp = newData.iloc[i,2]
        if temp not in uniques:
            uniques.append(temp)
    #find minimum of unique num set
    tmin = min(uniques)
    for i in range(0, newData.shape[0]):
            newData.iloc[i,3] = int(newData.iloc[i,2]) - tmin    #IMPORTANT: labels have to go from 0-(max)
    #features/labels
    x = newData.drop(['RS'], axis = 1)
    y = newData['RS']
    #split beween test, train
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2)

    feature_columns = []
    feature_columns.append(feature_column.numeric_column('Shot_location'))
    feature_columns.append(feature_column.numeric_column('Save_type'))
    #build model
    learning_rate=0.001
    if (tf.__version__[0] == '2'):
        optimizer_adam= tf.optimizers.Adam(learning_rate=learning_rate)
    else:
        optimizer_adam= tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)
    hidden_units=[37,30,19]
    #SIZE OF UNIQUE STUFF SET
    model=tf.estimator.DNNClassifier(hidden_units=hidden_units, feature_columns=feature_columns,  optimizer=optimizer_adam, n_classes=len(uniques))
    model.train(input_fn=lambda: input_fn(features=x_train, labels=y_train, training=True), steps=1000)
    testing_results = model.evaluate(input_fn=lambda: input_fn(features=x_test, labels=y_test, training=False), steps=1)
    ptemp = list(model.predict(input_fn=lambda: input_fn(features=x_test, labels=y_test, training=False)))
    probabilities = []
    for i in range(len(ptemp)):
        probabilities.append(ptemp[i])
    #make this a for loop if you want to see them all
    nums = probabilities[0]["probabilities"]
    print(testing_results)
    return model

#activ for neural net
def input_fn(features, labels, training=True, batch_size=32 ):
    dataf = tf.data.Dataset.from_tensor_slices((dict(features), labels))
    if training:
        dataf = dataf.shuffle(200).repeat()
    return dataf.batch(batch_size=batch_size)

def singlePredict(model, loc, typ):
    data = [[loc,typ,1]]
    df = pd.DataFrame(data, columns = ['Shot_location', 'Save_type','Rebound_Bin'])
    df2= df['Rebound_Bin']
    ptemp = list(model.predict(input_fn=lambda: input_fn(features=df, labels=df2, training=False)))
    nums = ptemp[0]["probabilities"]
    return nums

def startup():
    importData()
    processData()
    model = analyzeData()
    return model

importData()
processData()
#analyzeData()
model = analyzeData()
#predict based on single point, change the params (shot_location, save_type respectively based on GUI input)
singlePredict(model, 1,1)
