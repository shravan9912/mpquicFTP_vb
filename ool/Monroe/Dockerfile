FROM monroe/base

MAINTAINER Jonas.Karlsson@kau.se

COPY files/quicse.sh /opt/monroe/
COPY go /root/go
COPY files/mptcp_up /etc/network/if-up.d/
COPY files/mptcp_down /etc/network/if-post-down.d/
COPY files/sources.list /etc/apt/

RUN apt-get update -y\
    && DEBIAN_FRONTEND=noninteractive apt-get install -f -y \
       libhdf5-serial-dev\ 
    && wget https://redirector.gvt1.com/edgedl/go/go1.9.2.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.9.2.linux-amd64.tar.gz \
    && rm go1.9.2.linux-amd64.tar.gz 

ENTRYPOINT ["dumb-init", "--", "/bin/bash", "/opt/monroe/quicse.sh"]
