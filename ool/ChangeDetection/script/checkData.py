from __future__ import division
import BayesianDetection.online_changepoint_detection as oncd
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import cProfile
import pandas as pd
#0.17.1
#0.22.0
import time

start = time.time()

rr = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_1.csv")
#ecf = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_2.csv")
#peek = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_1.csv")

#rr5 = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_2.csv")
#ecf5 = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_1.csv")
#peek5 = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_2.csv")

#rr10 = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_1.csv")
#ecf10 = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_2.csv")
#peek10 = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_1.csv")

#rr11 = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_2.csv")
#ecf11 = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_1.csv")
#peek11 = pd.read_csv("/home/mosaic/edge-computing-mpquic/output/detectionAgent_2.csv")
#result = pd.concat([(rr), (ecf), (peek), (rr5), (ecf5), (peek5), (rr10), (ecf10), (peek10), (rr11), (ecf11), (peek11)], axis=0, ignore_index=True)
#print(result)
#ax = seaborn.lineplot(data=result)
#plt.show()
#print(pd.__version__)
train_img_array = np.array([])
train_img_array =rr['PathInfo'].values
data = np.atleast_2d(train_img_array).T
#print(data)
R, maxes = oncd.online_changepoint_detection(data, partial(oncd.constant_hazard, 250), oncd.StudentT(0.1, .01, 1, 0))
#import matplotlib.cm as cm
#fig, ax = plt.subplots(figsize=[18, 16])
#ax = fig.add_subplot(3, 1, 1)
#ax.plot(data)
#ax = fig.add_subplot(3, 1, 2, sharex=ax)
#sparsity = 5  # only plot every fifth data for faster display
##ax.plot(np.array(range(0, len(R[:,0]), sparsity)))
#ax.pcolor(np.array(range(0, len(R[:,0]), sparsity)), 
#          np.array(range(0, len(R[:,0]), sparsity)), 
#          -np.log(R[0:-1:sparsity, 0:-1:sparsity]), 
#          cmap=cm.Greys, vmin=0, vmax=30)
#ax = fig.add_subplot(3, 1, 3, sharex=ax)
Nw=50;
i = 0
for element in R[Nw,Nw:-1]:
    if element > 0.5:
        i += 1
print(i)
end = time.time()
print(end - start)
#print(len(R[Nw,Nw:-1]))
#ax.plot(R[Nw,Nw:-1])
#plt.show()
