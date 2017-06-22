FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get upgrade -y
RUN apt-get install -y vim vim-common vim-runtime
RUN apt-get install -y python python-pip
RUN apt-get install -y git
RUN apt-get install -y gunicorn

