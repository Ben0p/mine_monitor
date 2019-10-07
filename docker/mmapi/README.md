# flask-boilerplate
Minimal setup for building a Python API running with Flask and MongoDB, inside Docker Containers. Some more info can be found in [this medium post](https://medium.com/@gabimelo/developing-a-flask-api-in-a-docker-container-with-uwsgi-and-nginx-e089e43ed90e).


## flask-app
Copy flask app contents into /src/server.py
Ensure app is "app" and not "APP" or "API" 

## Running it:

```
docker-compose build
docker-compose up -d
```

