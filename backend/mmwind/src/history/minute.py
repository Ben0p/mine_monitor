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

        DB['wind_history'].update(
            {
                'module_uid': anemometer['module_uid'],
                'range': anemometer['range']
            },
            {
                '$set': {
                    'module_uid': anemometer['module_uid'],
                    'range': anemometer['range'],
                },
                '$push': {
                    'datapoints': {
                        '$each' : anemometer['datapoints']
                        }
                },
            },
            upsert=True
        )


def purge(DB):

    time_now = datetime.datetime.now()
    time_minute = time_now - datetime.timedelta(minutes=1)

    DB['wind_history'].update(
        {
            'range': 'minute',
        },
        {
            '$pull': {
                'datapoints': {
                    'timestamp': {
                        '$lte': time_minute
                    },
                }
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

