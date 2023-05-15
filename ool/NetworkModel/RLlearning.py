import time
import argparse
from basicTopo import setup_environment

SERVER_CMD = "/home/mosaic/edge-computing-mpquic/quic/server_mt"
CERTPATH = "--certpath /home/mosaic/edge-computing-mpquic/quic/quic_go_certs"
SCH = "-scheduler dqnAgent"
ARGS = "-bind :6121 -www /home/mosaic/edge-computing-mpquic/www/"
COMMON = "-spec /home/mosaic/edge-computing-mpquic/quic/agent.spec -outputpath /home/mosaic/edge-computing-mpquic/output/"
TRAINING = "-training"
WFILE = "-weightsFile %s"
EPS = "-epsilon %s"
END = "> /home/mosaic/edge-computing-mpquic/logs/server.logs 2>&1"

BASIC_DELAY = 20

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

    #s1.cmd("./scripts/set_delay.bash %d" % int((BASIC_DELAY + rtt) / 2))
    #client.cmd("./scripts/client_set_delay.bash %d" % int((BASIC_DELAY + rtt) / 2))

    if tcp_traffic:
        client.cmd(TCP_CLIENT_CMD0)
        client.cmd(TCP_CLIENT_CMD1)

    start = time.time()
    client.sendCmd(CLIENT_CMD)
    # Timeout of 20 seconds for detecting crashing tests
    output = client.monitor(timeoutms=20000)

    # Check for timeout
    if client.waiting:
        delta = 20
        client.sendInt()
        client.waiting = False
        network.stop()
         #time.sleep(1)
         #network.cleanup()
    else:
        # TODO: Check for errors here?? How??
        delta = time.time() - start

    server.sendInt()

    server.monitor()
    server.waiting = False
    network.stop()


def do_training(is_training, weight_file, epsilon, rtt=0, tcp_b=False):
    server_cmd = " ".join([SERVER_CMD, CERTPATH, SCH, ARGS, COMMON])
    if is_training:
        server_cmd = " ".join([server_cmd, TRAINING])
    if epsilon is None:
        epsilon = 0.
    server_cmd = " ".join([server_cmd, WFILE % weight_file, EPS % epsilon, END])

    exec_test(server_cmd, rtt, tcp_b)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Executes a test with DQNAgent scheduler')
    parser.add_argument('--train', dest="training", action="store_true", help='indicates a training test')
    parser.add_argument('--weight_file', dest="wfile", help="path to weights file", required=False)
    parser.add_argument('--epsilon', dest="epsilon", help="epsilon while training", required=False)
    parser.add_argument('--rtt', type=int, dest="rtt", help="rtt primary leg")
    parser.add_argument('--background-tcp', dest="tcp_background", action="store_true", help='generates TCP background traffic during tests')

    args = parser.parse_args()
    do_training(args.training, args.wfile, args.epsilon, args.rtt, args.tcp_background)
