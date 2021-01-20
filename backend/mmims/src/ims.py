from env.sol import env

import pymongo
import requests
import json
import time
import urllib3

# Disable unsigned cert warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def auth():
    ''' Authenticates with API
    '''

    s = requests.Session()
    s.post(env.ims_auth_url, json={"username": env.ims_username, "password" : env.ims_password}, verify=False)

    return(s)


def initMongo():
    ''' Initialize MongoDB connection
        Returns connection
    '''
    
    CLIENT = pymongo.MongoClient(f"mongodb://{env.mongodb_ip}:{env.mongodb_port}")
    DB = CLIENT[env.database]

    return(DB)


def getAssests(s, DB):
    ''' Retrieve asset list from API
    '''

    assets = s.get(env.ims_assets_url, verify=False)
    assets = assets.json()

    for asset in assets:

        DB['ims_assets'].find_one_and_update(
            {
                'id' : asset['id'],
            },
            {
                '$set': asset
            },
            upsert=True
        )


def getLocations(s, DB):
    ''' Retrieve latest locations from API
    '''

    locations = s.get(env.ims_locations_url, verify=False)
    locations = locations.json()

    for location in locations:

        DB['ims_locations'].find_one_and_update(
            {
                'asset_id' : location['asset_id'],
            },
            {
                '$set': location
            },
            upsert=True
        )



def run():

    while True:

        session = auth()
        DB = initMongo()

        while True:

            try:

                # Asset list
                getAssests(session, DB)
                print("Retrieved assets")

                # Locations
                getLocations(session, DB)
                print("Retrieved locations")

                print("Sleep 60 sec")
                time.sleep(60)

            except json.decoder.JSONDecodeError:
                print("Exception, re-authenticating.")
                break
        
        time.sleep(60)





if __name__ == '__main__':
    run()