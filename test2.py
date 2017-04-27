#-*-coding:utf-8-*-
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import csv
import time
from datetime import datetime
from collections import Counter
import sys

def readCsv():
    with open('train.csv','rb') as f:
        reader = csv.DictReader(f,['id','date','loc'])
        for v in reader:
            yield v['date'],v['loc']

def weekday(string):
    #print string
    if string[0] != '2':
        return None
    string = string[:10]
    string = datetime.strptime(string,'%Y-%m-%d')
    return string.date().weekday()

def hourTime(string):
    string = string[11:13]
    return int(string)

def processData():
    locationsIndex=['01','02','03','04','05','06','07','08','09','10','11','12','13','14',\
          '15','16','17','18','19','20','21','22','23','24','25','26','27','28',\
          '29','30','31','32','33','34','35','36']
    timeIndex = pd.date_range('20150701','20151031',freq='H')
    data = np.zeros((len(locationsIndex),len(timeIndex)),np.int32)

    start = time.time()
    counter = Counter(readCsv())
    end = time.time()
    print 'counter takes %fs seconds' % (end - start)

    start = time.time()
    for i,loc in enumerate(locationsIndex):
        for j,tempTime in enumerate(timeIndex):
            data[i,j] = counter[tempTime.strftime('%m%d%H'),loc]
        print i
    end = time.time()
    print 'counter takes %fs seconds' % (end - start)
    
    df = pd.DataFrame(data,locationsIndex,timeIndex)
    return df

    
def clipSave(df,columsLength):
    times = columsLength/(7*24)
    clipPosition = 0
    frameDict = {}
    for i in range(times):
        
        frameDict[i] = df.iloc[:,1+i*7*24:1+(i+1)*7*24]
        #filestr = 'out_'+str(i)+'.csv'
        #frameDict[i].to_csv(filestr)
    return frameDict

def clip9to10(df):
    cols = df.columns.tolist()
    print np.array(cols)
    temp = '2015-09-07 00:00:00'
    index91 = cols.index(temp)
    #print index91
    saveFd = df.iloc[:,index91:]
    saveFd.to_csv('out2.csv')
    return saveFd

def clip10to10(df):
    cols = df.columns.tolist()
    print np.array(cols)
    temp = '2015-09-28 00:00:00'
    index91 = cols.index(temp)
    #print index91
    saveFd = df.iloc[:,index91:]
    saveFd.to_csv('out3.csv')
    return saveFd

def Plot(df):
    #df.ix[35].plot()
    #df.ix[34].plot()
    df.ix[15].plot()
    plt.show()

def getResultMat(frameDict):
    resultMat = np.zeros((36,7*24))
    dictLen = len(frameDict)
    for i in range(dictLen):
        values1 = frameDict[i].values
        if i != 5 and i!=4 and i!= 3 and i!=2 and i!=6:
            resultMat += values1
    resultMat /=(dictLen-5)             #       3
    return resultMat

def adaptResultToData(cols,data,resultMat):
    for i in range(len(cols)):
        weekd = weekday(str(cols[i]))
        hour = int(str(cols[i])[11:13])
        data[:,i] = resultMat[:,weekd*24+hour]
    return data

def saveDataToResultFile(data,locationsIndex,timeIndex):
    resultList=[]
    for i,loc in enumerate(locationsIndex):
        for j,time in enumerate(timeIndex):
            temp = str(time.strftime("%m%d%H"))
            #print temp
            templist = [str(i+1),str(temp),str(data[i,j])]
            strtemplist = str(i+1)+','+str(temp)+','+str(data[i,j])
            resultList.append(templist)
        #print i
    print len(resultList)
    fileMat = np.mat(resultList)
    print fileMat

    with open('result_2.csv','w') as f:
        for row in fileMat:
            np.savetxt(f,row,delimiter=',',fmt='%s')

def returnWeekResult(df):
    weekDict = {}
    locs,times,counts = 36,7*24,0
    for i in xrange(locs):
        timeDict = {}
        for j in xrange(times):
            countsDict={}
            for k in xrange(counts):
                countsDict[k] = 0
            timeDict[j] = countsDict
        weekDict[i] = timeDict
    
    weekResult = np.zeros((36,7*24))
    weekResultFlag = np.zeros((7*24,1))
    cols = df.columns[1:]
    for item in cols:# time index
        weekd = weekday(item)
        hour = hourTime(item)
        timeIndex = int(weekd) * 24 + hour
        for locationInd in df.index:    #loc index
            #print locationInd
            if len(weekDict[locationInd][timeIndex]) == 0:
                counts = 1
            else :
                counts = len(weekDict[locationInd][timeIndex]) + 1
            weekDict[locationInd][timeIndex][counts] = df[item][locationInd]

    print weekDict[0][115]
    for item in cols:# time index
        weekd = weekday(item)
        hour = hourTime(item)
        timeIndex = int(weekd) * 24 + hour
        for locationInd in df.index:    #loc index
            tempSeries = pd.Series(weekDict[locationInd][timeIndex])
            #print tempSeries
            a = sorted(tempSeries.values)
            if a[-1]-a[-2] > 100:
                a = a[:-1]
            if a[0] == 0 and len(a)>1:
                a = a[1:]
            
            #print a,"var:",np.var(a)
            
            if np.var(a)<1700:
                mid = np.mean(a)
            else:
                if len(a)==1 or len(a)==3 or len(a) ==5:
                    mid = a[len(a)/2]
                else:
                    if len(a)==2:
                        mid = np.mean(a)
                    elif len(a)==4:
                        mid = np.mean(a[1:3])
                    elif len(a)==6:
                        mid = np.mean(a[2:4])
                    else:
                        print a
            
            #print mid
            weekResult[locationInd][timeIndex] = mid
            #if locationInd == 12:
            #    sys.exit(0)
        #weekResultFlag[timeIndex] += 1
        #weekResult[:,timeIndex] += df[item]
    #print weekResult
    #print weekResultFlag
   # weekResult = weekResult//weekResultFlag.T
    print weekResult
    return weekResult
    
        
    
#######################
######S T A R T #######
#######################

try:
    df = pd.read_csv('out2.csv')
except:
    df = processData()
    df.to_csv('out.csv')

#print df['2015-10-12 09:00:00']
#print df.columns
Plot(df)
#print type(__file__),__file__,os.path.abspath(__file__)
#sys.exit(0)
clipTimeStripList=[]
clipList = ['2015-09-21','2015-10-01','2015-10-02','2015-10-03','2015-10-04','2015-10-05',\
            '2015-10-06','2015-10-07','2015-10-12','2015-10-13','2015-10-14','2015-09-30',]
ClipTimeIndex = pd.date_range('2015-09-21','2015-09-21',freq='H')
for item in clipList:
    start = str(item + ' 00:00:00')
    end = str(item +' 23:00:00')
    temptimeIndex = pd.date_range(start,end,freq='H')
    
    ClipTimeIndex+=(temptimeIndex)
    #ClipTimeIndex = ClipTimeIndex[1:]
print ClipTimeIndex
for item in ClipTimeIndex:
    del df[str(item)]
    
Plot(df)
df = clip10to10(df)
Plot(df)
#sys.exit(0)
retWeekResult = returnWeekResult(df)
df = pd.DataFrame(retWeekResult)
print df
Plot(df)                            #       1
#df = clip9to10(df)

locationsIndex=['01','02','03','04','05','06','07','08','09','10','11','12','13','14',\
          '15','16','17','18','19','20','21','22','23','24','25','26','27','28',\
          '29','30','31','32','33','34','35','36']
timeIndex = pd.date_range('2015-11-01 00:00:00','2015-11-30 23:00:00',freq='H')
data = np.zeros((len(locationsIndex),len(timeIndex)),np.int32)
cols = timeIndex.tolist()
data = adaptResultToData(cols,data,df.values)
print data

resultframe = pd.DataFrame(data,locationsIndex,timeIndex)
print timeIndex

Plot(resultframe)

saveDataToResultFile(data,locationsIndex,timeIndex)

sys.exit(0)
input1 = input("sss")


##################################

cols = df.columns.tolist()[1:]
columsLength = len(cols)
#print cols

frameDict = clipSave(df,columsLength)            #       2

locationsIndex=['01','02','03','04','05','06','07','08','09','10','11','12','13','14',\
          '15','16','17','18','19','20','21','22','23','24','25','26','27','28',\
          '29','30','31','32','33','34','35','36']
timeIndex = pd.date_range('2015-11-01 00:00:00','2015-11-30 23:00:00',freq='H')

resultMat = getResultMat(frameDict)

#resultMat = df.values
print resultMat
#input1 = input("sss")
data = np.zeros((len(locationsIndex),len(timeIndex)),np.int32)


cols =timeIndex.tolist()
#print cols[0],cols[1],type(cols[0]),str(cols[0]),len(cols)
data = adaptResultToData(cols,data,resultMat)

print data

resultframe = pd.DataFrame(data,locationsIndex,timeIndex)
print timeIndex

Plot(resultframe)

saveDataToResultFile(data,locationsIndex,timeIndex)




#print col
#df_clip = df.iloc[:,col:]


