from env.sol import env

import datetime
import pymongo
from bson import ObjectId

def formatData(anemometers):
    '''
    '''
    formatted = []

    # Iterate new anemometer data
    for key, value in anemometers.items():
        # Set initial dictionary values
        data = {}
        data['module_uid'] = ObjectId(key)
        data['range'] = 'minute'
        data['datapoints'] = []
        for datapoint in value['datapoints']:
            data['datapoints'].append(datapoint)
        formatted.append(data)
    return(formatted)


def insertDB(DB, formatted):

    for anemometer in formatted:

        for datapoint in anemometer['datapoints']:

            timestamp = datapoint['timestamp']
            second = timestamp.strftime('%Y%m%d%H%M%S')

            DB['wind_history'].find_one_and_update(
                {
                    'module_uid': anemometer['module_uid'],
                    'range': anemometer['range'],
                    'second': second
                },
                {
                    '$set':
                        {
                            'module_uid': anemometer['module_uid'],
                            'range': anemometer['range'],
                            'second': second,
                            'timestamp': timestamp,
                            'time' : datapoint['time'],
                            'ms': datapoint['ms'],
                            'kmh': datapoint['kmh'],
                            'knots': datapoint['knots'],
                        },
                },
                upsert=True
            )


def purge(DB):

    local_time = datetime.datetime.now() + datetime.timedelta(hours=env['local_offset'])

    DB['wind_history'].delete_many(
        {
            'range': 'minute',
            'timestamp': {
                '$lte': local_time - datetime.timedelta(minutes=2)
            }
        },
    )


def process(DB, anemometers):
    ''' Takes anemometer list of dictionaries
        Processes current minute data
        Inserts into historical data collection 
    '''

    formatted = formatData(anemometers)
    insertDB(DB, formatted)
    purge(DB)
