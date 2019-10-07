FROM python:3.7-alpine

RUN apt-get update

COPY ./requirements.txt /project/requirements.txt

RUN pip3 install -r /project/requirements.txt

COPY src /app/src

WORKDIR /app

CMD ["/usr/bin/supervisord"]
