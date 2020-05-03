from env.sol import env

import time
import pymongo



# Initialize mongo
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]




def pollOdroid(ip, station):

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




def main():

    while True:
        # Get odroid IP addresses
        odroids = DB['fm_odroids'].find()

        for odroid in odroids:
            data = pollOdroid(odroid['ip'], odroid['station'])


            DB['fm_live'].find_one_and_update(
                    {
                        'station' : data['station'],
                    },
                    {
                        '$set': {
                            'station' : data['station'],
                            'time': data['time'],
                            'artist': data['artist'],
                            'song' : data['song'],
                            'state' : data['state']
                        }
                    },
                    upsert=True
                )

            timestamp = f"{time.strftime('%d/%m/%Y %X')}"
            print(f"{timestamp} - Polled {data['station']}")
            
        
        time.sleep(10)









if __name__ == '__main__':
    main()