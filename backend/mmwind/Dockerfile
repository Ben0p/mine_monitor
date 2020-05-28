FROM python:3.8-alpine

# Install apt packages
RUN apt-get update && apt-get install -y \
    freetds-bin \
    freetds-common \
    freetds-dev

RUN pip install Cython
RUN pip install ipython
RUN pip install SQLAlchemy
RUN pip install pandas
RUN pip install Alembic

# Add source directory to Docker image
# Note that it's beneficial to put this as far down in the Dockerfile as
# possible to maximize the chances of being able to use image caching
ADD . /opt/src/pymssql/

RUN pip install /opt/src/pymssql

COPY src /app

WORKDIR /app/src

CMD ["python", "-u", "windy.py"]
