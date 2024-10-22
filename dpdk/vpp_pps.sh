#!/bin/bash

set -e

port=$1
interval=$2

[ "$interval"x != ""x ]  || interval=5
[ "$port"x != ""x ]  || port="GigabitEthernet2/0/0"

get_rx() {
  vppctl show int $port | grep 'rx packets' | awk '{print $7}' | tr -d '\t\n\r'
}

get_tx() {
  vppctl show int $port | grep 'tx packets' | awk '{print $3}' | tr -d '\t\n\r'
}

get_rb() {
  vppctl show int $port | grep 'rx bytes' | awk '{print $3}' | tr -d '\t\n\r'
}

get_tb() {
  vppctl show int $port | grep 'tx bytes' | awk '{print $3}' | tr -d '\t\n\r'
}

do_loop() {
  prev_rx=$(get_rx)
  prev_tx=$(get_tx)
  prev_rb=$(get_rb)
  prev_tb=$(get_tb)
  printf "\t\t\t\tRx packets/s\tTx packets/s\tRx Kib/s\tTx Kib/s\n"
  while true; do
    sleep $interval

    curr_rx=$(get_rx)
    curr_tx=$(get_tx)
    curr_rb=$(get_rb)
    curr_tb=$(get_tb)

    now=$(date --rfc-3339=second)
    rx_pps=$(( (curr_rx - prev_rx) / interval ))
    tx_pps=$(( (curr_tx - prev_tx) / interval ))
    rx_kps=$(( (curr_rb - prev_rb) / interval / 128 ))
    tx_kps=$(( (curr_tb - prev_tb) / interval / 128 ))

    printf "%-12s\t%-10s\t%-10s\t%-8s\t%-8s\t%s\n" "$now" $rx_pps $tx_pps $rx_kps $tx_kps

    prev_rx=$curr_rx
    prev_tx=$curr_tx
    prev_rb=$curr_rb
    prev_tb=$curr_tb
  done
}

do_loop
