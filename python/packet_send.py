#!/usr/bin/python3

import socket
import argparse
import time
import ipaddress
import multiprocessing


interval = 100
burst = 10000
udp_port = 0


def send_once(sock, start_ip, end_ip):
    cursor = start_ip
    for i in range(0, burst):
        cursor += 1
        cursor = min(cursor, end_ip)
        sock.sendto(b'from packet_send.py: ' +
                f'dest: {cursor}, port: {udp_port + i}'.encode(), (str(cursor), udp_port + i))


def loop_forever(segment):
    start_ip = segment[0]
    end_ip = segment[1]

    print('Running in [', start_ip, ',', end_ip, ']')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    while True:
        last_at = time.time()
        send_once(sock, start_ip, end_ip)
        elapsed = time.time() - last_at
        print(time.ctime(), 'Send packets during ', elapsed * 1000, 'ms')
        if elapsed < interval:
            time.sleep(interval - elapsed)


def split_address_space(start_ip, end_ip, chunk_size, count):
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)

    segments = []
    for i in range(0, count):
        if start >= end:
            start = ipaddress.IPv4Address(start_ip)
        current_end = min(start + chunk_size - 1, end)
        segments.append((ipaddress.IPv4Address(start), ipaddress.IPv4Address(current_end)))
        start = current_end + 1

    return segments


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-ip', default='192.0.0.2', help='ip address start at')
    parser.add_argument('--end-ip', default='192.255.255.254', help='ip address end at')
    parser.add_argument('--udp-port', default=99, type=int, help='port number for udp packet')
    parser.add_argument('--burst', default=10000, type=int, help='burst packet size')
    parser.add_argument('--interval', default=10.0, type=float, help='seconds of period')
    parser.add_argument('--threads', default=2, type=int, help='number of threads')

    args = parser.parse_args()

    burst = args.burst
    interval = args.interval
    threads = args.threads

    end = args.end_ip
    start = args.start_ip
    udp_port = args.udp_port

    segments = split_address_space(start, end, burst, threads)
    processes = []
    for i in segments:
        processes.append(multiprocessing.Process(target=loop_forever, args=(i,)))

    for process in processes:
        process.start()

    for process in processes:
        process.join()

