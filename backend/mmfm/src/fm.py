from env.sol import env

import time
import pymongo
import datetime

from devices import exstreamer500, odroid


def cleanUp(DB):
    fm_live = DB['fm_live'].find()

    for live in fm_live:
        count = DB['fm_modules'].count_documents(
            {
                'station': live['station']
            }
        )

        if count < 1:
            try:
                DB['fm_live'].delete_many(
                    {'module_uid': live['module_uid']}
                )
                print(f"Deleted {live['station']}")
            except:
                pass
            try:
                DB['fm_live'].delete_many(
                    {'station': live['station']}
                )
                print(f"Deleted {live['station']}")
            except:
                pass
def main():

    # Initialize mongo
    CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
    DB = CLIENT[env['database']]

    while True:
        # Clean up
        cleanUp(DB)
        # Get fm streaming modules ips and stations
        modules = DB['fm_modules'].find()

        # Iterate over modules
        for module in modules:
            # Odroids
            if module['type'] == 'Odroid':
                # Try (if online it will time out)
                try:
                    # Get live info from the odroid MongoDB
                    odroid_data = odroid.poll(module['ip'])
                    # Calc time offset, if the fm service has crashed the timestamp will be stale
                    try:
                        t_minus = time.time() - odroid_data['unix']
                        if t_minus > 10:
                            odroid_data['state'] = 'Offline'
                    except KeyError:
                        t_minus = 32949
                        odroid_data['unix'] = time.time()

                    # Convert to time delta and roud to seconds
                    odroid_data['t_minus'] = str(datetime.timedelta(seconds=round(t_minus)))
                except:
                    # If modules times out (offline)
                    odroid_data = {
                        'station' : '',
                        'time': '',
                        'artist': '',
                        'song' : '',
                        'state' : 'Offline',
                        'unix' : '',
                        't_minus' : '',
                    }

            try:
                # Push to live collection
                DB['fm_live'].find_one_and_update(
                        {
                            'station' : odroid_data['station'],
                        },
                        {
                            '$set': {
                                'station' : odroid_data['station'],
                                'url' : odroid_data['url'],
                                'time': odroid_data['time'],
                                'artist': odroid_data['artist'],
                                'song' : odroid_data['song'],
                                'state' : odroid_data['state'],
                                'unix' : odroid_data['unix'],
                                't_minus' : odroid_data['t_minus'],
                                'module_uid' : str(module['_id']),
                            }
                        },
                        upsert=True
                    )
            except:
                pass

            timestamp = f"{time.strftime('%d/%m/%Y %X')}"
            print(f"{timestamp} - Polled {odroid_data['station']}")
        
        time.sleep(10)


if __name__ == '__main__':
    main()