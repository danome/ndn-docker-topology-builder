#! /bin/bash
logfile="startup_ran.txt"
java_logfile=java.log
touch $logfile

metrics_dir=/metrics/$HOSTNAME
mkdir $metrics_dir -p

rewritten_nlsr_file=/nlsr.conf

declare -a default_ips=("172.19.0.10" "172.19.0.11" "172.19.0.12" "172.19.0.13" "172.19.0.14" "172.19.0.15" "172.19.0.16" "192.168.1.10")
declare -a default_nodenames=("a" "b" "c" "d" "e" "f" "g" "x")

echo "Starting nfd"
tmux new-session -s "nfd" -d
tmux send-keys -t "nfd" "nfd -c $NFD_CONFIG 2>&1 | tee /metrics/$HOSTNAME/nfd.log" Enter

# Give NFD and other nodes a second to start
sleep 20s

echo "Starting ping server"
tmux new-session -s "ping" -d 
tmux send-keys -t "ping" "ndnpingserver /com/stefanolupo/ndngame/0/$HOSTNAME" Enter 

echo "Setting strategies"
nfdc strategy set /com/stefanolupo/ndngame /localhost/nfd/strategy/best-route/%FD%01
nfdc strategy set /com/stefanolupo/ndngame/0/discovery/broadcast /localhost/nfd/strategy/multicast/%FD%03

echo "Adding default faces"
for i in "${default_nodenames[@]}"
do
    face="udp://node$i.ndngame.com"
    echo "Creating face: " $face
    nfdc face create $face
done

echo "Rewriting NLSR"
java -jar node-rewriter.jar $NLSR_CONFIG $rewritten_nlsr_file

echo "Starting NLSR"
tmux new-session -s "nlsr" -d 
tmux send-keys -t "nlsr" "nlsr -f $rewritten_nlsr_file" Enter


if [ -n "$GAME" ]; then
    echo "Starting game" > $logfile
    tmux new-session -s "game" -d 
    tmux send-keys -t "game" "$GAME 2>&1 | tee $metrics_dir/$java_logfile" Enter
else
    echo "Starting as router" > $logfile
fi