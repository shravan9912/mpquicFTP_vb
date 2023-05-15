import pandas

minrtt = pandas.read_csv("/home/mosaic/edge-computing-mpquic/output/minrtt.csv")
ecf = pandas.read_csv("/home/mosaic/edge-computing-mpquic/output/ecf.csv")
result = pandas.concat([(minrtt), (ecf)], axis=1)
print(result)

import matplotlib.pyplot as plt

color = {'boxes': 'DarkGreen', 'whiskers': 'DarkOrange','medians': 'DarkBlue', 'caps': 'Gray'}

result.plot.box(color=color,fontsize=18)

plt.ylabel("Time (ms)", fontsize=20)
#plt.ylim(top=4000)
plt.xlabel("Schedulers", fontsize=20)
#plt.show()
plt.savefig('./result.png')
