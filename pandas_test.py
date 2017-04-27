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

index = [1,2,3,4,5]
cols = ['studytime','playtime',3]
data = np.ones((len(index),len(cols)),np.int32)
data[0,:] = [1,5,4]
data[1,:] = [3,5,6]
data[3,:] = [32,15,16]
df = pd.DataFrame(data,index=index,columns = cols)
print df.describe()
df2 = df[3].groupby(df['studytime']).apply(lambda p :p.describe())
print df2
a = dict()
print a
