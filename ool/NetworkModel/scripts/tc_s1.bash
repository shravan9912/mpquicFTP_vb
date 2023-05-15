#!/usr/bin/env bash

tc qdisc add dev s1-eth1 root handle 5:0 hfsc default 1
tc class add dev s1-eth1 parent 5:0 classid 5:1 hfsc sc rate 150Mbit ul rate 150Mbit
tc qdisc add dev s1-eth1 parent 5:1 netem loss 0.1% delay 14ms 2ms

tc qdisc add dev s1-eth2 root handle 5:0 hfsc default 1
tc class add dev s1-eth2 parent 5:0 classid 5:1 hfsc sc rate 80Mbit ul rate 80Mbit
tc qdisc add dev s1-eth2 parent 5:1 netem loss 0.1% delay 15ms 2ms

# tc qdisc add dev s1-eth1 root handle 5:0 hfsc default 1
# tc class add dev s1-eth1 parent 5:0 classid 5:1 hfsc sc rate 150Mbit ul rate 150Mbit
# tc qdisc add dev s1-eth1 parent 5:1 netem loss 0.1% delay 14ms 2ms

# tc qdisc add dev s1-eth2 root handle 5:0 hfsc default 1
# tc class add dev s1-eth2 parent 5:0 classid 5:1 hfsc sc rate 30Mbit ul rate 30Mbit
# tc qdisc add dev s1-eth2 parent 5:1 netem loss 0.3% delay 10ms 2ms

# tc qdisc add dev s1-eth1 root handle 5:0 hfsc default 1
# tc class add dev s1-eth1 parent 5:0 classid 5:1 hfsc sc rate 80Mbit ul rate 80Mbit
# tc qdisc add dev s1-eth1 parent 5:1 netem loss 0.1% delay 15ms 2ms

# tc qdisc add dev s1-eth2 root handle 5:0 hfsc default 1
# tc class add dev s1-eth2 parent 5:0 classid 5:1 hfsc sc rate 30Mbit ul rate 30Mbit
# tc qdisc add dev s1-eth2 parent 5:1 netem loss 0.3% delay 10ms 2ms
