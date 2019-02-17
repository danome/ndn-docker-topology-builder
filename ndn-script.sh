cxx_repo="https://github.com/named-data/ndn-cxx.git"
cxx_release_tag="ndn-cxx-0.6.5"
cxx_dir="ndn-cxx"

nfd_repo="https://github.com/named-data/NFD.git"
nfd_release_tag="NFD-0.6.5"
nfd_dir="nfd-0.6.5"

chronosync_repo="https://github.com/named-data/ChronoSync.git"
chronosync_release_tag="0.5.2"
chronosync_dir="chronosync-0.5.2"

psync_repo="https://github.com/named-data/PSync.git"
psync_release_tag="0.1.0"
psync_dir="psync-0.1.0"

function install() {
  git_repo=$1
  tag=$2
  release_dir_name=$3

  git clone --depth 1 --branch $tag $git_repo
  cd $release_dir_name
  
  ./waf distclean
  echo "Finished cleaning"

  ./waf configure
  echo "Finished configuring, compiling"

  ./waf -j2
  echo "Finished compiling, installing"

  sudo ./waf install
}

sudo apt update
sudo apt install python

# NDN Cxx
sudo apt install build-essential libsqlite3-dev libboost-all-dev libssl-dev
install $cxx_repo $cxx_release_tag $cxx_dir
sudo ldconfig

# NFD
sudo apt-get install pkg-config libpcap-dev
install $nfd_repo $nfd_release_tag $nfd_dir

# # Use initial config file for now
sudo cp /usr/local/etc/ndn/nfd.conf.sample /usr/local/etc/ndn/nfd.conf

# # Create the NFD service
# sudo cp nfd.service /etc/systemd/system/
# sudo systemctl start nfd.service
# sudo systemctl enable nfd.service

# # Install ChronoSync
install $chronosync_repo $chronosync_release_tag $chronosync_dir

# # Install PSync
install $psync_repo $psync_release_tag $psync_dir
