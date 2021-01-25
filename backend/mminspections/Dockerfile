FROM python:3.9-alpine

RUN apk update

COPY ./requirements.txt /project/requirements.txt

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python -m pip install -r /project/requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY src /app

WORKDIR /app/src

CMD ["python", "-u", "inspect.py"]
