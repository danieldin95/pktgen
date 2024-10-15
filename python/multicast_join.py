#!/usr/bin/python3

import time
import argparse

from scapy.all import sendp
from scapy.all import Ether, IP
from scapy.contrib.igmp import IGMP


def run(group, iface="eth0", interval=15):
    """"""
    a = Ether()
    b = IP()
    c = IGMP(type=0x12, gaddr=group)
    x = a/b/c
    x[IGMP].igmpize()

    while True:
        sendp(x, iface=iface)
        time.sleep(interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--group', default="239.0.0.1", 
                        help="Multicast group address in CIDR 224.0.0.0/4")
    parser.add_argument('--iface', default="eth0",
                        help="Interface where send IGMP packet in, default is eth0")
    parser.add_argument('--interval', type=int, default=15,
                        help="The interval in seconds send IGMP packet next times")
    args = parser.parse_args()
    run(args.group, args.iface, args.interval)

