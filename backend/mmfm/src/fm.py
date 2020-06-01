from env.sol import env

import time
import pymongo

from devices import exstreamer500, odroid



def main():

    # Initialize mongo
    CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
    DB = CLIENT[env['database']]

    while True:
        # Get odroid IP addresses
        modules = DB['fm_modules'].find()

        for module in modules:
            if module['type'] == 'Odroid':
                odroid_data = odroid.poll(module['ip'], module['station'])

            DB['fm_live'].find_one_and_update(
                    {
                        'station' : odroid_data['station'],
                    },
                    {
                        '$set': {
                            'station' : odroid_data['station'],
                            'time': odroid_data['time'],
                            'artist': odroid_data['artist'],
                            'song' : odroid_data['song'],
                            'state' : odroid_data['state']
                        }
                    },
                    upsert=True
                )

            timestamp = f"{time.strftime('%d/%m/%Y %X')}"
            print(f"{timestamp} - Polled {module['station']}")
            
        
        time.sleep(10)









if __name__ == '__main__':
    main()