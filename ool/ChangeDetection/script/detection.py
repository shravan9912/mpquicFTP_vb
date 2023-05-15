#!/usr/bin/python

#fr = open("./test", "r")
#line = fr.readline()
#print "Read Line: %s" % (line)
from __future__ import division
import BayesianDetection.online_changepoint_detection as oncd
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import cProfile
import pandas as pd
import time
import os.path
from os import path

start_time = time.time()
prev = int(0)
while True:
    fr = open("./DumpDataPointer", "r")
    line = fr.readline()
    num = int(line)
    if num == -1 or time.time() - start_time > 10:
        break
    time.sleep(0.01)
    #avoid dirty reading
    if num > prev and path.isfile("/home/mosaic/edge-computing-mpquic/output/detectionAgent_"+str(num)+".csv"):
    #if num == (prev + 1) or num == (prev + 2):
        prev = num
        #print("        ",num)
        rr = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_"+str(prev)+".csv")
        #do somthing here and then notify mpquic
        train_img_array = np.array([])
        train_img_array =rr['PathInfo'].values
        data = np.atleast_2d(train_img_array).T
        R, maxes = oncd.online_changepoint_detection(data, partial(oncd.constant_hazard, 250), oncd.StudentT(0.1, .01, 1, 0))
        #do somthing here and then notify mpquic
        Nw=50;
        i = 0
        for element in R[Nw,Nw:-1]:
            if element > 0.85:
                i += 1
        print("Chang point is " ,i)
        if i > 1:
            fo = open("./CheckNotificationPointer", "w")
            fo.write(str(1))
            fo.close()
            while True:
                fw = open("./CheckNotificationPointer", "r")   
                wline = fw.readline()
                wnum = int(wline)
                if wnum == int(0):
                    break
                else:
                    time.sleep(0.005)
                    fr = open("./DumpDataPointer", "r")
                    line = fr.readline()
                    num = int(line)
                    if num == -1 or time.time() - start_time > 10:
                        break
#fo = open("./CheckNotificationPointer", "w")
#fo.write(str(0))
#fo.close()
