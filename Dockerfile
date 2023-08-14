FROM ubuntu:20.04 

#python:3.7-buster

RUN mkdir --parents /home/ibf
ENV HOME /home/ibf
WORKDIR $HOME


RUN apt-get update && \
	apt-get install -y python3-pip && \
	ln -sfn /usr/bin/python3.10 /usr/bin/python && \
	ln -sfn /usr/bin/pip3 /usr/bin/pip


RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    software-properties-common \
    nano \
    vim \
	python3-eccodes \
    git \
    wget \
    libxml2-utils \
    gir1.2-secret-1\
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge --auto-remove \
    && apt-get clean 


RUN add-apt-repository ppa:ubuntugis/ppa \
    && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    python-numpy \
    gdal-bin \
    libgdal-dev \
    postgresql-client \
		libproj-dev \
    libgeos-dev \
	libspatialindex-dev \
    libudunits2-dev \
    libssl-dev \
    libgnutls28-dev \    
    libeccodes0 \
		libcairo2-dev\
		libgirepository1.0-dev\
    gfortran \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge --auto-remove \
    && apt-get clean

#####################
# install blobfuse2

RUN apt-get update \
    && apt-get install -y wget apt-utils \
    && wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && apt-get update \
    && apt-get install -y libfuse3-dev fuse3 

RUN apt-get update && apt-get -y upgrade \   
    && apt-get install -y blobfuse2



#############
RUN apt-get update && apt-get -y upgrade && \
    apt-get -f -y install curl apt-transport-https lsb-release gnupg && \
    curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.asc.gpg && \
    CLI_REPO=$(lsb_release -cs) && \
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ ${CLI_REPO} main" \
    > /etc/apt/sources.list.d/azure-cli.list && \
    apt-get update && \
    apt-get install -y azure-cli && \
    rm -rf /var/lib/apt/lists/*
	
# update pip
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
RUN chmod 755 /home/ibf/azure-blobfuse-mount.sh
RUN chmod +x /home/ibf/azure-blobfuse-mount.sh
#ENTRYPOINT ["bash","/home/ibf/azure-blobfuse-mount.sh"]
RUN pip install .



 
