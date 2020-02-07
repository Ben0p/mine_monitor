from env.sol import env
import requests
import json
import time
import pymongo

# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]


url = 'http://ws1.theweather.com.au/?lt=uwas&lc=183,179,180,574,570,1443,1442&alerts=1(client=337)&format=json&u=15566-1804&k=805a6dfa9a03c4e22c8dce2277c06c30'


while True:

    lightnings = []

    response = requests.get(url = url)
    json_data = json.loads(response.text)
    
    locations = json_data['countries'][0]['locations']

    for location in locations:


        DB['alert_ww'].find_one_and_update(
            {
                'name': location['name']
            },
            {
                '$set': {
                    'name' : location['name'],
                    'status' : location['alerts'][0]['status']
                }
            },
            upsert=True
        )




    time.sleep(60)



