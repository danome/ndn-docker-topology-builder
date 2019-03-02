#! /bin/bash
touch startup_ran.txt

declare -a default_ips=("172.19.0.10" "172.19.0.11" "172.19.0.12" "172.19.0.13" "172.19.0.14" "172.19.0.15" "172.19.0.16" "192.168.1.10")

echo "Starting nfd"
tmux new-session -s "nfd" -d "nfd"

echo "Adding default faces"
for i in "${default_ips[@]}"
do
    nfdc face create udp://$i
done

echo "Starting NLSR"
tmux new-session -s "nlsr" -d "nlsr -f $NLSR_CONFIG"