#-*-coding:utf-8-*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
import csv
from collections import Counter

try:
    dd = pd.read_msgpack('data.msgpack')

except ValueError:
    def csv_counter():
        with open('train.csv') as f:
            reader=csv.DictReader(f,['id','date','loc'])
            for v in reader:
                yield v['date'], v['loc']



    def date_parser(string):
        return datetime.strptime('2016'+string, '%Y%m%d%H')
    ##
    ##tic = time.time()
    ##data = list(csv_counter())
    ##toc = time.time()
    ##print('[*] 璇诲彇csv鐢ㄦ椂 %fs'%(toc - tic))


    tic = time.time()
    # counter = Counter(data)
    counter = Counter(csv_counter())
    toc = time.time()
    print('[*] 璁℃暟鐢ㄦ椂 %fs'%(toc - tic))

    DatetimeIndex = pd.date_range('20160701', '20161031',freq='H')
    # LocationColum = sorted(list(set(k[1] for k in data)))
    LocationColum = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']

    M = np.zeros((len(DatetimeIndex), len(LocationColum)), np.int32)

    tic = time.time()
    for j, loc in enumerate(LocationColum):
        for i,T in enumerate(DatetimeIndex):
            M[i, j] = counter[T.strftime('%m%d%H'), loc]
        print(j)
    toc = time.time()
    print('[*] M鐭╅樀鐢熸垚鐢ㄦ椂 %fs'%(toc - tic))

    dd=pd.DataFrame(M, DatetimeIndex, LocationColum)
    
dd.plot(y='25')
plt.show()

import sklearn
import sklearn.gaussian_process
gpr=sklearn.gaussian_process.GaussianProcessRegressor()
