from __future__ import division
import online_changepoint_detection as oncd
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import cProfile
import offline_changepoint_detection as offcd
import generate_data as gd

dim = 1
if dim == 1:
  partition, data = gd.generate_normal_time_series(4, 50, 200)
else:
  partition, data = gd.generate_multinormal_time_series(7, dim, 50, 200)
print(data)

R, maxes = oncd.online_changepoint_detection(data, partial(oncd.constant_hazard, 250), oncd.StudentT(0.1, .01, 1, 0))

import matplotlib.cm as cm
fig, ax = plt.subplots(figsize=[18, 16])
ax = fig.add_subplot(2, 1, 1)
ax.plot(data)
ax = fig.add_subplot(2, 1, 2, sharex=ax)
# sparsity = 5  # only plot every fifth data for faster display
# #ax.plot(np.array(range(0, len(R[:,0]), sparsity)))
# ax.pcolor(np.array(range(0, len(R[:,0]), sparsity)), 
#           np.array(range(0, len(R[:,0]), sparsity)), 
#           -np.log(R[0:-1:sparsity, 0:-1:sparsity]), 
#           cmap=cm.Greys, vmin=0, vmax=30)
# ax = fig.add_subplot(3, 1, 3, sharex=ax)
Nw=50;
print(R[Nw,Nw:-1])
print(len(R[Nw,Nw:-1]))
ax.plot(R[Nw,Nw:-1])
print(partition)
plt.savefig("loss.pdf", bbox_inches='tight')
plt.show()



