#!/usr/bin/env bash

tc qdisc change dev client-eth0 parent 5:1 netem loss 28.19% delay $1ms 19ms
