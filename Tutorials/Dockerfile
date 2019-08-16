FROM ubuntu:latest

ENV hostname 172.20.10.2
ENV hostname 172.17.0.1 
ENV hostname 172.18.0.1

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install python3
RUN python3 -V
RUN sudo apt-get install -y python3-pip
RUN pip3 -V
RUN pip3 install virtualenv
RUN virtualenv --version
RUN mkdir django-apps
RUN cd django-apps
RUN virtualenv env
RUN . env/bin/activate
RUN pip3 install django
RUN django-admin --version
