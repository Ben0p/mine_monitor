FROM python:3.7-alpine

RUN apk update
RUN apk add --no-cache python3-dev libstdc++ && \
    apk add --no-cache g++ && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h

COPY ./requirements.txt /project/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r /project/requirements.txt

COPY src /app

WORKDIR /app/src

CMD ["python", "-u", "fm.py"]
