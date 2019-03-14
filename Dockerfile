# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM ubuntu:16.04

LABEL Name=FaceRecognition Version=0.0.1

WORKDIR /app

RUN apt-get update \
&& apt-get install -y python3-dev python3-pip \
&& cd /usr/local/bin \
&& ln -s /usr/bin/python3 python

RUN apt-get install -y libpq-dev libjpeg62 libjpeg62-dev cmake git
RUN apt-get install -y libfontconfig1 libxrender1 libglib2.0-0 libsm6 libxext6

# Build dblib from source
RUN git clone https://github.com/davisking/dlib.git
RUN cd dlib && mkdir build && cd build && cmake .. && cmake --build .

# Set locale for installing dependecy
RUN apt-get install -y locales \ 
&& rm -rf /var/lib/apt/lists/* \
&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

# Install and run pipenv
RUN python -m pip install pipenv
# Copy Pipfile or requirements.txt
#COPY ./requirements.txt /app
COPY ./Pipfile /app
RUN pipenv install
