FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get upgrade
RUN apt-get install -y vim vim-common vim-runtime
RUN apt-get install -y python python-pip
RUN apt-get install -y git
RUN apt-get install -y gunicorn

RUN git clone https://github.com/alliance-genome/agr.git /app

WORKDIR /app
RUN git checkout docker-integration

WORKDIR /app/api

RUN pip install -r requirements.txt
RUN nosetests -s test

WORKDIR /app/api/src

CMD gunicorn server:app -b 0.0.0.0:5000 -k gevent --pid ../gunicorn.pid --log-config ../docker/logging.conf
