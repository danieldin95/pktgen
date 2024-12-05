#!/usr/bin/python3

import time
import argparse
import subprocess

from scapy.all import sendp
from scapy.all import Ether, IP
from scapy.contrib.igmp import IGMP
from scapy.contrib.igmpv3 import IGMPv3, IGMPv3mr, IGMPv3gr


def get_address(name):

    output = subprocess.check_output(["ip", "addr", "show", name], encoding="utf-8")
    mac = None
    addr = None
    for line in output.splitlines():
        values = line.strip().split()
        if not mac and values[0] == "link/ether":
            mac = values[1]
        elif not addr and values[0] == "inet":
            addr = values[1].split('/')[0]
    return mac, addr


def run(group, iface="eth0", interval=15, ver="v3"):
    """"""
    mac, addr = get_address(iface)
    a = Ether(src=mac)
    b = IP(src=addr)

    if ver == "v1":
        c = IGMP(type=0x12, gaddr=group)
        x = a/b/c
        x[IGMP].igmpize()
    elif ver == "v3":
        g = IGMPv3gr(
            rtype=2,  # EXCLUDE 模式
            maddr=group,
        )
        c = IGMPv3(type=0x22)/IGMPv3mr(records=[g])
        x = a/b/c

    while True:
        sendp(x, iface=iface)
        time.sleep(interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--group', default="239.0.0.1", 
                        help="multicast group address")
    parser.add_argument('--version', default="v3",
                        help="igmp version v1 or v3")
    parser.add_argument('--iface', default="eth0",
                        help="interface send at")
    parser.add_argument('--interval', type=int, default=15,
                        help="interval seconds")
    args = parser.parse_args()

    run(args.group, args.iface, args.interval, args.version)

