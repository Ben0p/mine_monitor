import requests
from random import randrange
import time

base = 'http://localhost:5000/api/wind/'




while True:
    random_speed = randrange(10)
    params = f'get?mac=0080A3D488E0&name=Test&directionS=0&directionV=45.0&speedS=0&speedV={random_speed}'
    full_string = f'{base}{params}'
    requests.get(url = full_string)

    print(full_string)

    time.sleep(60)



