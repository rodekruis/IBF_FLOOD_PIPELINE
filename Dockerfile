FROM python:3.7-buster

RUN mkdir --parents /home/ibf
ENV HOME /home/ibf
WORKDIR $HOME

RUN apt-get update && \
	apt-get install -y python3-pip && \
	ln -sfn /usr/bin/python3.6 /usr/bin/python && \
	ln -sfn /usr/bin/pip3 /usr/bin/pip

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN deps='build-essential gdal-bin python-gdal libgdal-dev kmod wget apache2' && \
	apt-get update && \
	apt-get install -y $deps

RUN pip install --upgrade pip && \
	pip install GDAL==$(gdal-config --version)

RUN apt-get update\
    && apt-get install -y curl

RUN apt-get update && apt-get -y upgrade && \
    apt-get -f -y install curl apt-transport-https lsb-release gnupg python3-pip python-pip && \
    curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.asc.gpg && \
    CLI_REPO=$(lsb_release -cs) && \
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ ${CLI_REPO} main" \
    > /etc/apt/sources.list.d/azure-cli.list && \
    apt-get update && \
    apt-get install -y azure-cli && \
    rm -rf /var/lib/apt/lists/*
	
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

 
