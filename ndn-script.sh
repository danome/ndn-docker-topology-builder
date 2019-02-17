cxx_release="https://github.com/named-data/ndn-cxx/archive/ndn-cxx-0.6.5.tar.gz"
cxx_file_name="ndn-cxx-0.6.5.tar.gz"
cxx_dir="ndn-cxx-0.6.5"

nfd_release="https://github.com/named-data/NFD/archive/NFD-0.6.5.tar.gz"
nfd_file_name="NFD-0.6.5.tar.gz"
nfd_dir="nfd-0.6.5"

chronosync_release="https://github.com/named-data/ChronoSync/archive/0.5.2.tar.gz"
chronosync_filename="chronosync-0.5.2.tar.gz"
chronosync_dir="chronosync-0.5.2"

psync_release="https://github.com/named-data/PSync/archive/0.1.0.tar.gz"
psync_filename="psync-0.1.0.tar.gz"
psync_dir="psync-0.1.0"

function install() {
  release=$1
  release_file_name=$2
  release_dir_name=$3
  wget $release -O $release_file_name
  mkdir -p $release_dir_name && tar -zxvf $release_file_name -C $release_dir_name --strip-components 1
  cd $release_dir_name
  ./waf distclean
  ./waf configure
  echo "Finished configuring, compiling"
  ./waf -j2
  echo "Finished compiling, installing"
  sudo ./waf install
}

# NDN Cxx
# sudo apt install build-essential libsqlite3-dev libboost-all-dev libssl-dev
# install $cxx_release $cxx_file_name $cxx_dir
# sudo ldconfig

# NFD
sudo apt-get install build-essential pkg-config libboost-all-dev \
                     libsqlite3-dev libssl-dev libpcap-dev
install $nfd_release $nfd_file_name $nfd_dir

# # Use initial config file for now
# sudo cp /usr/local/etc/ndn/nfd.conf.sample /usr/local/etc/ndn/nfd.conf

# # Create the NFD service
# sudo cp nfd.service /etc/systemd/system/
# sudo systemctl start nfd.service
# sudo systemctl enable nfd.service

# # Install ChronoSync
# install $chronosync_release $chronosync_filename $chronosync_dir

# # Install PSync
# install $psync_release $psync_filename $psync_dir
