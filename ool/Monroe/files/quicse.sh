 #!/bin/bash
 #ifdown eth0
 #ifdown op0
 #sleep 2
 #ip route > /monroe/results/iproutedown.txt
 #ip rule show > /monroe/results/ipruleshowdown.txt
 #ifup eth0
 #ifup op0
 #sleep 2 
 cat /etc/apt/sources.list
 cat /etc/os-release
 /usr/local/go/bin/go version 
 cd /root/go/src/github.com/lucas-clemente/quic-go/example/client_benchmarker/
 /usr/local/go/bin/go build main.go
 #ls 
 #ls
 #cd /usr/lib/
 #ls
 cp ./main ./root/go/bin/client_benchmarker
 #ifconfig
 cd /root/go/bin/
 #ls
 ./client_benchmarker -m https://128.39.37.146:6121/512k
 #ip route > /monroe/results/iproute.txt
 #ip rule show > /monroe/results/ipruleshow.txt
 #ip route show table 10000 > /monroe/results/iproute10000.txt
 #ip route show table 10001 > /monroe/results/iproute10001.txt  
