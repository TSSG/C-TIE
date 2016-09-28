# C-TIE Cloud based Traffic Identification Engine
C-TIE is a cloud hosted deep packet inspection application which can be used to identify applications in use on a network by examining the content of the packet payloads.

## Install Instructions
To install C-TIE follow the instructions below.

    # System has been tested on Ubuntu 14.04, with Python 2.7.x
    # Access to an ActiveMQ server is required. The configuration for ActiveMQ can be updated in the start.py script.

    # Install the project dependencies
    sudo apt-get install python-pip python-dev python-twisted libjson0 libjson0-dev libpcap-dev autoconf automake libpcap-dev libtool build-essential bison flex byacc libperl-dev libgtk2.0-dev
    sudo pip install stompest stompest.async service_identity

    # Initialise the git submodules:
    git submodule init
    git submodule update

    # To compile the nDPI library:
    cd nDPI
    ./autogen.sh
    ./configure
    make

    # To compile wireshark:
    cd wireshark
    ./autogen.sh
    ./configure
    make


## Launch Instructions
To launch the C-TIE application simply:

    python start.py

### Ingress Message Format
The format of a message expected by C-TIE in the ingress queue can be seen in the following example packet payload:

    {
      "payload": "92e76b51c3f952540012350208004500002c00850000400660930a25027e0a0003120016b4fd0084d001c87de2876012ffff4dc30000020405b40000"
    }

### Egress Message Format
The format of the message returned by C-TIE when an attempt to identify a packet has been made is as follows:

    {
      "dpi_response": {
        "detected.protos": [
          {
            "bytes": 60,
            "breed": "Acceptable",
            "packets": 1,
            "name": "SSH",
            "flows": 1
          }
        ],
        "traffic.statistics": {
          "pppoe.pkts": 0,
          "udp.pkts": 0,
          "pkt.len_1024_1500": 0,
          "tcp.pkts": 1,
          "vlan.pkts": 0,
          "unique.flows": 1,
          "pkt.len_min64": 1,
          "max.pkt.size": 24,
          "ip.bytes": 60,
          "pkt.len_grt1500": 0,
          "ip.packets": 1,
          "discarded.bytes": 0,
          "mpls.pkts": 0,
          "avg.pkt.size": 60,
          "pkt.len_256_1024": 0,
          "pkt.len_128_256": 0,
          "ethernet.bytes": 84,
          "total.packets": 1,
          "pkt.len_64_128": 0,
          "fragmented.pkts": 0,
          "guessed.flow.protos": 1
        },
        "known.flows": []
      },
      "payload": "92e76b51c3f952540012350208004500002c00850000400660930a25027e0a0003120016b4fd0084d001c87de2876012ffff4dc30000020405b40000"
    }


### Licence
GNU LESSER GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2016, TSSG, WIT.

### Contributors
The following people have contributed to this module:

- David Kirwan <dkirwan@tssg.org> / <davidkirwanirl@gmail.com>
