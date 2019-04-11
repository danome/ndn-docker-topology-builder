#! /bin/bash
logfile="startup_ran.txt"
java_logfile=java.log
touch $logfile

metrics_dir=/metrics/$HOSTNAME
mkdir $metrics_dir -p

rewritten_nlsr_file=/nlsr.conf

declare -a default_nodenames=("a" "b" "c" "d" "e" "f" "g" "h" "i" "j" "k" "l" "nn" "m" "n" "o" "p" "q" "r" "s" "t" "x")

echo "Starting nfd"
tmux new-session -s "nfd" -d
tmux send-keys -t "nfd" "nfd -c $NFD_CONFIG 2>&1 | tee /metrics/$HOSTNAME/nfd.log" Enter

# Give NFD and other nodes a second to start
sleep 120s
# sleep 20s

echo "Starting ping server"
tmux new-session -s "ping" -d 
tmux send-keys -t "ping" "ndnpingserver /$HOSTNAME" Enter 

echo "Setting strategies"
nfdc strategy set /com/stefanolupo/ndngame /localhost/nfd/strategy/best-route/%FD%01
# nfdc strategy set /com/stefanolupo/ndngame /localhost/nfd/strategy/multicast/%FD%03
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

# Sleep based on node name
# letter="${HOSTNAME:4}"
# lower=${letter,,}
# i=0
# sleepTime=0
# for item in "${default_nodenames[@]}"; do
#     if [[ $lower == "$item" ]]; then
#         sleepTime=$((10*i))
#         echo "$HOSTNAME sleeping for $sleepTime"
#         break
#     fi
#     i=$((i+1))
# done

# sleep ${sleepTime}s

if [ -n "$GAME" ]; then
    # Give NLSR a chance
    echo "Sleeping to give NLSR a chance"
    sleep 120s
    echo "Starting game" > $logfile
    tmux new-session -s "game" -d 
    tmux send-keys -t "game" "$GAME 2>&1 | tee $metrics_dir/$java_logfile" Enter
else
    echo "Starting as router" > $logfile
fi