#! /bin/bash
apt install software-properties-common -y && apt update
add-apt-repository ppa:named-data/ppa -y
apt install ndn-tools