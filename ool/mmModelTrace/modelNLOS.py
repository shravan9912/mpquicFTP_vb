#import sys
import time
import random
import math
import monotonic
import pandas as pd

LOS=1
NLOS=0
K=0.9449
gamma=0.4852
c_15=5.5547
T=(c_15*math.log(2))/K
cellusers=10
bw_value=180
d_2d=20
d_3d=d_2d
std_los = 4.0
std_nlos = 8.2
f_c= 28
bw_change_interval = 1 
timecheckproportion = 0.05
sinr = 20
PL_offset = 1
cellusers = 10
lambdaLosToNlos = 0.15

B_PL_los = 32.4 + 21*math.log10(d_3d) + 20*math.log10(f_c)
P_los = 18/d_2d + math.exp(-d_2d/36) * (1 - 18/d_2d)

if P_los > random.uniform(0,1):
    LOSstate = NLOS
else:
    LOSstate = NLOS
sleepremainder=0
t=0
sleepinc=bw_change_interval*timecheckproportion
f= open("/home/mosaic/edge-computing-mpquic/logs/marker.txt","r")
lines=f.readlines()
b = int(lines[0])
print(b)
f.close()
f= open("/home/mosaic/edge-computing-mpquic/logs/marker.txt","w+")
f.write("%d" % (17+1))
f.close()
i = 0
b = []

while True:
    i += 1
    new_t=monotonic.time.time()
    if LOSstate == LOS:
        mPathLoss = 32.4 + 21*math.log10(d_3d) + 20*math.log10(f_c)
        aPL = random.normalvariate(mPathLoss, std_los)
    else:
        mPathLoss = 32.4 + 31.9*math.log10(d_3d) + 20*math.log10(f_c) 
        aPL = random.normalvariate(mPathLoss, std_nlos)
    aPL = aPL + PL_offset * std_los  
    PL = aPL - B_PL_los
    C_mmwave = bw_value*K/math.log(2) * min(T,math.log(1+gamma*(10**((sinr-PL)/10)))) 
    C_ue=C_mmwave
    if 50 < i :
        break
    print(C_ue)
    b.append(C_ue)
    #print("./scripts/client_change.bash %s" % C_ue) 
    sleepremainder = sleepremainder - (new_t - t)
    t = new_t
    P_los = 18/d_2d + math.exp(-d_2d/36) * (1 - 18/d_2d) #initial probability of loss
    mu = P_los/(1-P_los) * lambdaLosToNlos
    if sleepremainder <= 0:
        if LOSstate == NLOS:
            losstatetime = random.expovariate(mu)
            LOSstate = NLOS
        else:
            losstatetime = random.expovariate(lambdaLosToNlos)
            LOSstate = NLOS
        print(LOSstate,losstatetime)
    else:
        losstatetime = sleepremainder
    if losstatetime < bw_change_interval:
        sleeptime = losstatetime
        sleepremainder = 0
    else:
        sleepremainder = losstatetime - bw_change_interval
        sleeptime = bw_change_interval
    startsleep=monotonic.time.time()
    while (monotonic.time.time()-startsleep) < sleeptime:
        time.sleep(sleepinc)

cars = {
        'Throughput': b
        }

df = pd.DataFrame(cars, columns= ['Throughput'])

df.to_csv ('modelNLOS.csv', index = False, header=True)

print (df)
