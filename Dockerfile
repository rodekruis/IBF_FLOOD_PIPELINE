FROM ubuntu:18.04

RUN mkdir --parents /home/ibf
ENV HOME /home/ibf
WORKDIR $HOME

RUN apt-get update && apt-get install -y \
    software-properties-common \
    nano \
    vim \
    python3-pip \
    git \
    wget \
    libxml2-utils \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge --auto-remove \
    && apt-get clean

RUN add-apt-repository ppa:ubuntugis/ppa \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
    python-numpy \
    gdal-bin \
    libgdal-dev \
    postgresql-client \
    libgnutls28-dev \
    libgnutls28-dev \
    libspatialindex-dev \
    libeccodes0 \
    gfortran \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge --auto-remove \
    && apt-get clean

# update pip
RUN python3 -m pip install --no-cache-dir \
    pip \
    setuptools \
    wheel \
    --upgrade \
    && python3 -m pip install --no-cache-dir numpy

 
# install dependencies
COPY requirements.txt /home/ibf
RUN pip install --no-cache-dir -r requirements.txt


# Copy code and install
ADD pipeline .
RUN pip install .

 
