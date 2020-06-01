FROM python:3.7-alpine

RUN apk update
RUN apk add curl gcc libc-dev g++ libffi-dev libxml2 unixodbc-dev mariadb-dev postgresql-dev
RUN apk add freetds freetds-dev

#Download the desired package(s)
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.5.2.2-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.5.2.1-1_amd64.apk

#Install the package(s)
RUN apk add --allow-untrusted msodbcsql17_17.5.2.2-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools_17.5.2.1-1_amd64.apk

#Python
RUN pip install --upgrade pip
RUN pip install pyodbc
RUN pip install pymongo

ADD odbcinst.ini /etc/odbcinst.ini

COPY src /app
WORKDIR /app/src
CMD ["python", "-u", "windy.py"]
