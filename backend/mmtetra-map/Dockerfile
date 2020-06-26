FROM python:3.7-alpine

RUN apk update

COPY ./requirements.txt /project/requirements.txt

RUN pip3 install -r /project/requirements.txt

COPY src /app

WORKDIR /app/src

CMD ["python", "-u", "tetra.py"]
