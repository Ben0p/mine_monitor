FROM joyzoursky/python-chromedriver:3.6-alpine3.7

RUN mkdir packages
ADD requirements.txt packages
RUN pip install -r packages/requirements.txt

COPY src /app

WORKDIR /app/src

CMD ["python", "-u", "weather.py"]
