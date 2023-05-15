import time
import random
import math
import monotonic
import pandas as pd
import datetime

Tracefile = "./modelDynamic.csv"
f= open("/home/mosaic/edge-computing-mpquic/logs/marker.txt","r")
lines=f.readlines()
b = int(lines[0])

data = pd.read_csv(Tracefile)
limit = len(data.index)

while True:
    if b < limit:  
        throughput = float(data.loc[b, 'Throughput'])
        print(b)
        b+=1
        cue = throughput/10
        print(cue)
    else:
        b = 0
        throughput = float(data.loc[b, 'Throughput'])
        print(b)
        b+=1
        cue = throughput/10
        print(cue)

f = open("/home/mosaic/edge-computing-mpquic/logs/marker.txt","w+")
f.write("%d" % b)
f.close()


