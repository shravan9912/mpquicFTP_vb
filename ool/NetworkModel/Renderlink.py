import datetime
import time
import random
import math
import monotonic
import argparse
import threading
import pandas as pd
from basicTopo import setup_environment

SERVER_CMD = "/home/mosaic/edge-computing-mpquic/quic/server_mt"
CERTPATH = "--certpath /home/mosaic/edge-computing-mpquic/quic/quic_go_certs"
SCH = "-scheduler %s"
ARGS = "-bind :6121 -www /home/mosaic/edge-computing-mpquic/www/"
END = "> /home/mosaic/edge-computing-mpquic/logs/server.logs 2>&1"
LOS_CAPACITY = 1

CLIENT_CMD = "/home/mosaic/edge-computing-mpquic/quic/client_mt -m https://10.0.0.20:6121/test3  > /home/mosaic/edge-computing-mpquic/logs/client.logs 2>&1"

TCP_SERVER_CMD = "cd /home/mosaic/edge-computing-mpquic/www && python -m SimpleHTTPServer 80 &"
TCP_CLIENT_CMD0 = "curl --interface client-eth0 -s -o /dev/null 10.0.0.20/test3 &"
TCP_CLIENT_CMD1 = "curl --interface client-eth1 -s -o /dev/null 10.0.0.20/test3 &"


def setup():
    net = setup_environment()
    net.start()
    return net


def exec_test(server_cmd, rtt, tcp_traffic):
    network = setup()

    s1 = network.get("s1")
    server = network.get("server")
    client = network.get("client")

    if tcp_traffic:
        server.cmd(TCP_SERVER_CMD)

    server.sendCmd(server_cmd)
    client.cmd("sleep 1")

    if tcp_traffic:
        client.cmd(TCP_CLIENT_CMD0)
        client.cmd(TCP_CLIENT_CMD1)

    client.sendCmd(CLIENT_CMD)
    print(client.shell)
    start = datetime.datetime.now()
    iii = 0
    while client.waiting:
        client.pexec("./scripts/client_change.bash %d" % int(LOS_CAPACITY))
        s1.pexec("./scripts/s1_change.bash %d" % int(LOS_CAPACITY))
        elapsed = datetime.datetime.now() - start
        if elapsed > datetime.timedelta(seconds=5):
            client.sendInt()
            client.waiting = False
        output = client.monitor(timeoutms=20)
        iii += 1
    print(iii)  
    print(client.shell)      
    #time.sleep(1)
    #client.pexec("./scripts/change_delay.bash %d" % int((BASIC_DELAY + rtt) / 2))
    # Timeout of 20 seconds for detecting crashing tests
    #output = client.monitor(timeoutms=20000)

    # Check for timeout
    #if client.waiting:
    #    delta = 20
    #    client.sendInt()
    #    client.waiting = False
    #    network.stop()
    #     #time.sleep(1)
    #     #network.cleanup()
    #else:
    #    # TODO: Check for errors here?? How??
    #    delta = time.time() - start

    server.sendInt()

    server.monitor()
    server.waiting = False
    network.stop()

# Define a function for the thread
def render_link():
    
    iii = 0
    global stop_threads
    global client
    global network
    global s1 

    bw_change_interval = 1.0
    timecheckproportion = 0.05
    cellusers = 10
    sleepinc=bw_change_interval*timecheckproportion

    #Tracefile = "../traceTest/modelLOS.csv"
    #Tracefile = "../traceTest/modelNLOS.csv"
    #Tracefile = "../traceTest/modelDynamic.csv"
    Tracefile = "../traceTest/TraceLOS.csv"
    #Tracefile = "../traceTest/TraceNLOS.csv"
    #Tracefile = "../traceTest/TraceDriving.csv"
    f= open("/home/mosaic/edge-computing-mpquic/logs/marker.txt","r")
    lines=f.readlines()
    b = int(lines[0])

    data = pd.read_csv(Tracefile)
    limit = len(data.index)

    while True:
        if b < limit:  
            throughput = float(data.loc[b, 'Throughput'])
            b+=1
        else:
            b = 0
            throughput = float(data.loc[b, 'Throughput'])
            b+=1
        C_ue=throughput/cellusers
        print("Bandwidth:" ,C_ue)
        client.pexec("./scripts/client_change.bash %s" % C_ue)
        s1.pexec("./scripts/s1_change.bash %s" % C_ue)
        iii += 1
        if stop_threads or (15 < iii) : 
            break  
        startsleep=monotonic.time.time()
        sleeptime = bw_change_interval
        while (monotonic.time.time()-startsleep) < sleeptime:
            time.sleep(sleepinc)        

    f = open("/home/mosaic/edge-computing-mpquic/logs/marker.txt","w+")
    f.write("%d" % b)
    f.close()    
    #print(iii)
    client.sendInt()
    client.waiting = False

def do_training(sch, rtt=0, tcp_b=False):
    server_cmd = " ".join([SERVER_CMD, CERTPATH, SCH % sch, ARGS, END])

    exec_test(server_cmd, rtt, tcp_b)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Executes a test with defined scheduler')
    parser.add_argument('--scheduler', dest="sch", help="Scheduler (rtt, random)", required=True)
    parser.add_argument('--rtt', type=int, dest="rtt", help="rtt primary leg")
    parser.add_argument('--background-tcp', dest="tcp_background", action="store_true",
                        help='generates TCP background traffic during tests')

    args = parser.parse_args()
    server_cmd = " ".join([SERVER_CMD, CERTPATH, SCH % args.sch, ARGS, END])

    network = setup()
    s1 = network.get("s1")
    server = network.get("server")
    client = network.get("client")

    server.sendCmd(server_cmd)
    client.cmd("sleep 1")

    stop_threads = False
    t1 = threading.Thread(target = render_link) 
    t1.start() 
    client.sendCmd(CLIENT_CMD)
    output = client.monitor(timeoutms=10000)   
    stop_threads = True
    t1.join() 
    
    server.sendInt()
    server.monitor()
    server.waiting = False
    network.stop()
