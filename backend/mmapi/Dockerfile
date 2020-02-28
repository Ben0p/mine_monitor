FROM python:3.7-alpine

RUN apk update && apk add libressl-dev postgresql-dev libffi-dev gcc musl-dev python3-dev 

COPY ./requirements.txt /project/requirements.txt

RUN pip3 install -r /project/requirements.txt

COPY src /app

WORKDIR /app/src

EXPOSE  5000

CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "wsgi:app"]
