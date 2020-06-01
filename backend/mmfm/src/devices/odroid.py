from env.sol import env

import time
import pymongo

def poll(ip, station):

    timestamp = f"{time.strftime('%d/%m/%Y %X')}"

    try:
        c = pymongo.MongoClient(f"mongodb://{ip}:{env['mongodb_port']}/")
        d = c['fm_stream']

        data = d['fm_live'].find_one()

    except:
        data = {
            'station' : station,
            'time' : timestamp,
            'artist' : '',
            'song' : '',
            'state' : 'Offline'
        }

    return(data)

