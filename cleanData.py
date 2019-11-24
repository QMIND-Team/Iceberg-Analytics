import csv,random
import pandas as pd

data = []

def importData():
    global data
    data = pd.read_csv("data/shotDataSample.csv")

def processData():
    global data
    #print (data[0][1]) #row, column
    toDelete = [1,3,6,7,9,18,19,20,23,24,25,26,27,28,29,33,34,36,37,41,42,43,44,45] #columns to delete
    toCopy = [0,2,4,5,8,10,11,12,13,14,15,16,17,21,22,30,31,32,35,38,39,40]
    #for i in toDelete
    data = data.drop(data.columns[toDelete],axis = 1)
    print (data)


importData()
processData()
