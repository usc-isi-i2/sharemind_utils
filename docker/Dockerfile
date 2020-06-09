FROM ubuntu:16.04
WORKDIR /root
RUN apt-get update && apt-get install -y \
  bison \
  cmake \
  doxygen \
  flex \
  g++ \
  gcc \
  git \
  libboost-dev \
  libboost-filesystem-dev \
  libboost-iostreams-dev \
  libboost-program-options-dev \
  libboost-system-dev \
  libbz2-dev \
  libcrypto++-dev \
  libgmp-dev \
  libgnutls28-dev \
  libhdf5-dev \
  libhiredis-dev \
  libmpfr-dev \
  libssl-dev \
  m4 \
  make \
  nettle-dev \
  patch \
  pkg-config \
  vim \
  wget \
  xz-utils
RUN apt-get install -y --no-install-recommends doxygen

# install conda
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    chmod +x Miniconda3-latest-Linux-x86_64.sh && \
    ./Miniconda3-latest-Linux-x86_64.sh -p /root/miniconda -b && \
    rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/root/miniconda/bin:${PATH}
RUN conda update -y conda

ADD source/ /root/source
ENV LD_LIBRARY_PATH /root/build-sdk/prefix/lib
#ADD README.md .
ADD install.sh .
RUN ["bash", "install.sh"]
CMD ["/bin/bash"]

