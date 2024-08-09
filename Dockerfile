
FROM python:3.10

RUN apt-get update
ARG DEBIAN_FRONTEND=nonnteractive


RUN apt-get -y install php-fpm php-mysql
# RUN pip install mysqlclient
RUN apt-get -y install default-mysql-client 
RUN apt-get -y install php-fpm php-mysql

RUN mkdir /src
COPY . /SocialSphere
WORKDIR /SocialSphere

COPY requirements.txt /src/requirements.txt


RUN groupadd -g 1003 sasi

RUN useradd -r -m -u 1010 -g sasi sasi
RUN rm -rf /var/lib/apt/lists/*
RUN pip install -r /src/requirements.txt
USER sasi


ENTRYPOINT "/SocialSphere/script/startScript.sh"

