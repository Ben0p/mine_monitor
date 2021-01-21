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

    return(assets)


def getLocations(s, DB):
    ''' Retrieve latest locations from API
    '''

    locations = s.get(env.ims_locations_url, verify=False)
    locations = locations.json()

    return(locations)


def updateLocation(assets, locations):
    ''' Looks up asset id in the locations and combines the two
    '''

    updated = []

    for asset in assets:
        # I don't know, copied this form stack overflow
        asset['location'] = next((item for item in locations if item["asset_id"] == asset['id']), None)

        updated.append(asset)

    return(updated)


def updateDB(DB, assets):
    ''' Upserts asssets with latest location into MongoDB
    '''

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



def run():

    while True:

        session = auth()
        DB = initMongo()

        while True:

            try:

                # Asset list
                assets = getAssests(session, DB)
                print("Retrieved assets")

                # Locations
                locations = getLocations(session, DB)
                print("Retrieved locations")

                # Combine location in to asset
                assets = updateLocation(assets, locations)
                print("Updated locations")

                # Updated DB
                updateDB(DB, assets)
                print("Updated DB")

                print("Sleep 60 sec")
                time.sleep(60)

            except json.decoder.JSONDecodeError:
                print("Exception, re-authenticating.")
                break
        
        time.sleep(60)





if __name__ == '__main__':
    run()