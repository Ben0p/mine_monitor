from env.sol import env

import datetime
import pymongo
from bson import ObjectId


def avg(speeds):
    try:
        average = sum(speeds) / len(speeds)
        average = round(average, 2)
    except ZeroDivisionError:
        average = 0

    return(average)


def getMinutes(DB):

    minutes = DB['wind_history'].find(
        {
            'range': 'minute'
        }
    )

    return(minutes)


def genMinuteList():
    ''' Generates list of minutes (HHMM) for the past hour
    '''

    minute_dicts = {}

    # Time now
    time_now = datetime.datetime.now()
    # I don't know
    start = time_now - datetime.timedelta(minutes=60)

    year = int(time_now.strftime('%Y'))
    month = int(time_now.strftime('%m'))
    day = int(time_now.strftime('%d'))

    first = time_now.strftime('%H')
    first = f"{first}00"
    first = int(first)

    last = start.strftime('%H')
    last = f"{last}60"
    last = int(last)

    start = start.strftime('%H%M')
    start = int(start)
    end = time_now.strftime('%H%M')
    end = int(end) + 1

    for i in range(start, last, 1):
        i = f'{i:04}'
        timestamp = datetime.datetime(year, month, day, int(i[:2]), int(i[-2:]))
        minute_dicts[i] = {
            'timestamp': timestamp,
            'time' : timestamp.strftime('%y/%m/%d %H:%M'),
            'kmh': [],
            'ms': [],
            'knots': []
        }

    for i in range(first, end, 1):
        i = f'{i:04}'
        timestamp = datetime.datetime(year, month, day, int(i[:2]), int(i[-2:]))
        minute_dicts[i] = {
            'timestamp': timestamp,
            'time' : timestamp.strftime('%y/%m/%d %H:%M'),
            'kmh': [],
            'ms': [],
            'knots': []
        }

    return(minute_dicts)


def formatData(DB, minutes, minute_dicts):

    for anemometer in minutes:
        # Set initial dictionary values
        data = {}
        data['module_uid'] = ObjectId(anemometer['module_uid'])
        data['range'] = 'hour'

        for datapoint in anemometer['datapoints']:
            minute = datapoint['timestamp']
            minute = minute.strftime('%H%M')
            try:
                minute_dicts[minute]['kmh'].append(datapoint['kmh'])
                minute_dicts[minute]['ms'].append(datapoint['ms'])
                minute_dicts[minute]['knots'].append(datapoint['knots'])
            except:
                pass

        for key, value in minute_dicts.items():

            DB['wind_history'].update(
                {
                    'module_uid': ObjectId(anemometer['module_uid']),
                    'range': 'hour'
                },
                {
                    '$set': {
                        'module_uid': ObjectId(anemometer['module_uid']),
                        'range': 'hour',
                        f'minutes.{key}.timestamp' : value['timestamp'],
                        f'minutes.{key}.time' : value['time'],
                    },
                    '$push': {
                        f'minutes.{key}.kmh': {
                            '$each': value['kmh']
                        },
                        f'minutes.{key}.ms': {
                            '$each': value['ms']
                        },
                        f'minutes.{key}.knots': {
                            '$each': value['knots']
                        }
                    },
                },
                upsert=True
            )


def averageData(DB):

    hour_data = DB['wind_history'].find(
        {
            'range': 'hour'
        }
    )

    for anemometer in hour_data:

        datapoints = []

        for key, value in anemometer['minutes'].items():
            data = {}

            timestamp = value['timestamp']
            time = value['time']

            if len(value['kmh']) > 0:

                kmh_avg = avg(value['kmh'])
                kmh_max = max(value['kmh'])
                kmh_min = min(value['kmh'])

                ms_avg = avg(value['ms'])
                ms_max = max(value['ms'])
                ms_min = min(value['ms'])
            
                knots_avg = avg(value['knots'])
                knots_max = max(value['knots'])
                knots_min = min(value['knots'])
            
            else:
                kmh_avg = 0
                kmh_max = 0
                kmh_min = 0

                ms_avg = 0
                ms_max = 0
                ms_min = 0
            
                knots_avg = 0
                knots_max = 0
                knots_min = 0
        

            data['timestamp'] = timestamp
            data['time'] = time
            data['kmh'] = {
                'min' : kmh_min,
                'avg' : kmh_avg,
                'max' : kmh_max
            }
            data['ms'] = {
                'min' : ms_min,
                'avg' : ms_avg,
                'max' : ms_max
            }
            data['knots'] = {
                'min' : knots_min,
                'avg' : knots_avg,
                'max' : knots_max
            }

            datapoints.append(data)
    

        DB['wind_history'].find_one_and_update(
            {
                'module_uid': anemometer['module_uid'],
                'range': anemometer['range']
            },
            {
                '$set': {
                    'module_uid': anemometer['module_uid'],
                    'range': anemometer['range'],
                    'datapoints' : datapoints
                }
            },
            upsert=True
        )

def purge(DB):

    time_now = datetime.datetime.now()
    time_hour = time_now - datetime.timedelta(minutes=60)

    anemometers = DB['wind_history'].find(
        {
            'range' : 'hour'
        }
    )

    for anemometer in anemometers:
        purged_minutes = {}

        minutes = anemometer['minutes']

        for key, value in minutes.items():
            if value['timestamp'] > time_hour:
                purged_minutes[key] = value

        DB['wind_history'].find_one_and_update(
            {
                'range': 'hour',
                'module_uid' : anemometer['module_uid']
            },
            {
                '$set' : {
                    'minutes' : purged_minutes
                }
            }
        )


def process(DB):

    minutes = getMinutes(DB)
    minute_dicts = genMinuteList()
    formatData(DB, minutes, minute_dicts)
    averageData(DB)
    purge(DB)
