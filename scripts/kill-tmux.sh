#! /bin/bash
tmls | awk -F ":" '{system("tmux kill-session -t" $1)}'