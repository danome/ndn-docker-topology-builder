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

nlsr_repo="https://github.com/named-data/NLSR.git"
nlsr_release_tag="NLSR-0.4.3"
nlsr_hash="85998a1dc942974a7d4bf3e9f642c5a22dffb6f8"
nlsr_dir="nlsr-0.4.3"

# Handy for checking for shared lib remenants from apt
# ldconfig -p | grep "ndn"

function install() {
  git_repo=$1
  tag=$2
  release_dir_name=$3

  git_command="git clone --depth 1 --branch $tag $git_repo $release_dir_name"

  
  if [ $git_repo == $nfd_repo ]
  then
    echo "Updating submodule for " $git_repo
    git submodule update --init
    git_command="$git_command --recursive"
  fi
  
  if [ $git_repo == $nlsr_repo ]
  then
    git clone $git_repo $release_dir_name
    cd $release_dir_name
    git checkout $nlsr_hash
  else
    $git_command
    cd $release_dir_name
  fi

  ./waf distclean
  echo "Finished cleaning"

  ./waf configure
  echo "Finished configuring, compiling"

  ./waf -j2
  echo "Finished compiling, installing"

  sudo ./waf install

  cd ../
}

# sudo add-apt-repository ppa:named-data/ppa -y

# sudo apt update && sudo apt install -y \
#   build-essential \
#   git \
#   libsqlite3-dev \
#   libboost-all-dev \
#   libssl-dev \
#   libpcap-dev \
#   pkg-config \
#   python \


# # NDN Cxx
# install $cxx_repo $cxx_release_tag $cxx_dir
# sudo ldconfig

# # NFD
# install $nfd_repo $nfd_release_tag $nfd_dir

# # Use initial config file for now
# sudo cp /usr/local/etc/ndn/nfd.conf.sample /usr/local/etc/ndn/nfd.conf

# # Create the NFD service
# sudo cp nfd.service /etc/systemd/system/
# sudo systemctl start nfd.service
# sudo systemctl enable nfd.service

# # Install ChronoSync
# install $chronosync_repo $chronosync_release_tag $chronosync_dir

# # Install PSync
# install $psync_repo $psync_release_tag $psync_dir

# Install NLSR
install $nlsr_repo $nlsr_release_tag $nlsr_dir

# sudo apt install ndn-tools -y
