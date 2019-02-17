FROM ubuntu:18.04
ARG VERSION_CXX="ndn-cxx-0.6.5"
ARG VERSION_NFD="NFD-0.6.5"
ARG VERSION_CHRONO_SYNC="0.5.2"
ARG VERSION_PSYNC="0.1.0"
ARG VERSION_NLSR="85998a1dc942974a7d4bf3e9f642c5a22dffb6f8"

# install tools
RUN apt update && apt install -y \
  build-essential \
  git \
  libsqlite3-dev \
  libboost-all-dev \
  libssl-dev \
  libpcap-dev \
  pkg-config \
  python

# install ndn-cxx
RUN git clone https://github.com/named-data/ndn-cxx.git \
    && cd ndn-cxx \
    && git checkout $VERSION_CXX \
    && ./waf configure \
    && ./waf \
    && ./waf install \
    && cd .. \
    && rm -Rf ndn-cxx \
    && ldconfig

# install NFD
RUN git clone --recursive https://github.com/named-data/NFD \
    && cd NFD \
    && git checkout $VERSION_NFD \
    && ./waf configure \
    && ./waf \
    && ./waf install \
    && cd .. \
    && rm -Rf NFD

# install ChronoSync
RUN git clone https://github.com/named-data/ChronoSync.git \
    && cd ChronoSync \
    && git checkout $VERSION_CHRONO_SYNC \
    && ./waf configure \
    && ./waf \
    && ./waf install \
    && cd .. \
    && rm -Rf ChronoSync

# install PSync
RUN git clone https://github.com/named-data/PSync.git \
    && cd PSync \
    && git checkout $VERSION_PSYNC \
    && ./waf configure \
    && ./waf \
    && ./waf install \
    && cd .. \
    && rm -Rf PSync

# install NLSR
RUN git clone https://github.com/named-data/NLSR.git \
    && cd NLSR \
    && git checkout $VERSION_NLSR \
    && ./waf configure \
    && ./waf \
    && ./waf install \
    && cd .. \
    && rm -Rf NLSR

# install ndn-tools
RUN git clone --recursive https://github.com/named-data/ndn-tools.git \
    && cd ndn-tools \
    && ./waf configure \
    && ./waf \
    && ./waf install \
    && cd .. \
    && rm -Rf ndn-tools

# initial configuration
RUN cp /usr/local/etc/ndn/nfd.conf.sample /usr/local/etc/ndn/nfd.conf \
    && ndnsec-keygen /`whoami` | ndnsec-install-cert - \
    && mkdir -p /usr/local/etc/ndn/keys \
    && ndnsec-cert-dump -i /`whoami` > default.ndncert \
    && mv default.ndncert /usr/local/etc/ndn/keys/default.ndncert

RUN mkdir /share \
    && mkdir /logs

# cleanup
RUN apt autoremove \
    && apt-get remove -y git build-essential python pkg-config

EXPOSE 6363/tcp
EXPOSE 6363/udp

ENV CONFIG=/usr/local/etc/ndn/nfd.conf
ENV LOG_FILE=/logs/nfd.log

CMD /usr/local/bin/nfd -c $CONFIG > $LOG_FILE 2>&1