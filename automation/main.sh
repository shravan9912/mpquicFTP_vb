export GOPRIVATE=github.com/shravan9912
#go build server.go
#cd client && go build client.go && cd ..
cd ..
set -a && source envs/mininet.env && set +a
sudo python mininettest/topo2_1.py
