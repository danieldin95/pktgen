#!/usr/bin/env python3


import time
import argparse
import sys
import subprocess
import re


def get_rx(port):
	data = {}
	pattern = r"rx_queue_(\d+)_packets"
	output = subprocess.check_output(["ethtool", "-S", port], encoding="utf-8")

	for line in output.splitlines():
		line = line.strip()
		match = re.search(pattern, line)
		if not match:
			continue
		values = line.split()
		if len(values) != 2:
			continue

		queue_number = match.group(1)
		data[queue_number] = int(values[1])
	return data


def once(last, now):
	sys.stdout.write("{}\n".format(time.ctime()))
	count = 0
	total = 0
	data = {}
	for key, value in last.items():
		data[key] = now[key] - value
	
	new_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
	for key, value in new_data.items():
		count += 1
		sys.stdout.write("%6s: %-8d" % (key, value))
		if count % 8 == 0:
			sys.stdout.write("\n")
		total += value

	if count % 8 != 0:
		sys.stdout.write("\n")
	
	sys.stdout.write("total: {}\n".format(total))


def loop(port, interval):
	last = get_rx(port)
	for i in range(0, 1024 * 1024):
		time.sleep(interval)
		now = get_rx(port)
		once(last, now)
		last = now


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--iface', default="eth0", 
		help="Interface name")
	parser.add_argument('--interval', default=2, type=int, 
		help="Interval seconds")
	args = parser.parse_args()

	loop(args.iface, args.interval)


if __name__ == '__main__':
	main()