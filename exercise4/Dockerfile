FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python 3.9 python3-pip
WORKDIR /saj
COPY ./app .
RUN pip3 install -r requirements.txt
CMD gunicorn --bind 0.0.0.0:8888 app:app
