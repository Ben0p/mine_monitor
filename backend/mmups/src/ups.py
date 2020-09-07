from env.sol import env

import pymongo
import time

from models import pxgx, nmc


# Initialize mongo
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]


def getUPSs():

    modules = DB['ups_modules'].find()
    return(modules)


def updateDB(ups):

    DB['ups_data'].insert_one(
        {
            'module_uid' : ups['module_uid'],
            "unix" : time.time(),
            "status" : ups['status'],
            "phases" : ups['phases'],
            "load_precent" : ups['load_percent'],
            "load_status" : ups['load_status'],
            "load_icon" : ups['load_icon'],
            "batt_remaining" : ups['batt_remaining'],
            "batt_status" : ups['batt_status'],
            "batt_icon" : ups['batt_icon'],
            "kw_out" : ups['kw_out'],
            "temp" : ups['temp'],
            "temp_status" : ups['temp_status'],
            "temp_icon" : ups['temp_icon'],
        }
    )


def truncate_data(seconds):
    ''' Delete UPS data older than 1 week
    '''

    DB['ups_data'].delete_many(
        {
            'unix' : {
                '$lte' : time.time() - seconds
            }
        },
    )


def poll():

    while True:
        upss = getUPSs()

        for ups in upss:

            print(f"Polling: {ups['name']}")

            if ups['type'] == 'PXGX':
                processed = pxgx.poll(ups)
            elif ups['type'] == 'NMC':
                processed = nmc.poll(ups)

            updateDB(processed)
        
        print("Truncate Data")
        truncate_data(604800)
        print("Sleep 10sec")
        time.sleep(10)

        
if __name__ == "__main__":

    poll()
    

