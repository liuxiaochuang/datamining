#-*-coding:utf-8-*-
#it has 16431540 items
import numpy as np
from matplotlib import pyplot as plt

                    #read first 10000 items in "train.csv"
def readCsv(filename, last_position, max_line):
    fileobj = open(filename,'rb')
    fileobj.seek(last_position)
    datalines = []
    for i in range(max_line):
        line_item = fileobj.readline()
        li=line_item.strip().split(',')
        datalines.append(li)
    return datalines

def judgeWeekday(date):
    monthDistance=int(date[:2])-7 #months 
    dateNum = int(date[2:4])
    time = int(date[4:6])
    if monthDistance == 0:
        dateNum += 0
    elif monthDistance == 1:
        dateNum += 31
    elif monthDistance == 2:
        dateNum += (31 + 31)
    elif monthDistance == 3:
        dateNum += (31 + 31 + 30)
    elif monthDistance == 4:
        dateNum += (31+31+30+31)
    elif monthDistance == 5:
        dateNum += (31+31 +30+31+31)

    weekdate = (dateNum+5-1)%7
    if weekdate == 0:
        weekdate = 7
    return weekdate,time

def initRoot(root):
    for weekday in root.values():
        for location in range(36):
            weekday[location] = []
            for time in range(24):
                weekday[location].append(0)

def countWeekday(root,item):
    weekday,time = judgeWeekday(item[1])
    time = int(time)
    location = int(item[2])
    #print weekday,location,type(location),time,type(time)
    root[weekday][location-1][time] += 1

def plotScatter(weekday):
    fig = plt.figure()
    for i in range(6):
        x1 = fig.add_subplot(2,3,i+1)
        x_1 = np.arange(24)
        x_2 = weekday[i+14]    
        x1.plot(x_2,'o--')
    plt.show()
    

data = readCsv('train.csv',0,100000)
matrix = np.array(data)

Monday={}
Tuesday = {}
Wednesday = {}
Thursday = {}
Friday = {}
Saturday = {}
Sunday = {}
root ={}
root[1] = Monday
root[2] = Tuesday
root[3] = Wednesday
root[4] = Thursday
root[5] = Friday
root[6] = Saturday
root[7] = Sunday
initRoot(root)
for item in matrix:
    countWeekday(root,item)
plotScatter(root[1])





