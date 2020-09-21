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


def getHours(DB):

    hours = DB['wind_history'].find(
        {
            'range': 'hour'
        }
    )

    return(hours)


def genHourList():
    ''' Generates list of hours (DDHH) for the past day
    '''

    hour_dicts = {}

    # Time now
    time_now = datetime.datetime.now()
    # I don't know
    start = time_now - datetime.timedelta(hours=24)

    year = int(time_now.strftime('%Y'))
    month = int(time_now.strftime('%m'))
    today = int(time_now.strftime('%d'))
    yesterday = int(start.strftime('%d'))

    first = time_now.strftime('%d')
    first = f"{first}00"
    first = int(first)

    last = start.strftime('%d')
    last = f"{last}24"
    last = int(last)

    start = start.strftime('%d%H')
    start = int(start)
    end = time_now.strftime('%d%H')
    end = int(end) + 1

    for i in range(start, last, 1):
        i = f'{i:04}'
        timestamp = datetime.datetime(year, month, yesterday, int(i[-2:]))
        hour_dicts[i] = {
            'timestamp': timestamp,
            'time' : f'{yesterday}/{month}/{year} {int(i[-2:])}:00',
            'kmh': [],
            'ms': [],
            'knots': []
        }

    for i in range(first, end, 1):
        i = f'{i:04}'
        timestamp = datetime.datetime(year, month, today, int(i[-2:]))
        hour_dicts[i] = {
            'timestamp': timestamp,
            'time' : f'{today}/{month}/{year} {int(i[-2:])}:00',
            'kmh': [],
            'ms': [],
            'knots': []
        }

    return(hour_dicts)


def formatData(DB, hours, hour_dicts):

    for anemometer in hours:
        # Set initial dictionary values
        data = {}
        data['module_uid'] = ObjectId(anemometer['module_uid'])
        data['range'] = 'day'

        for datapoint in anemometer['datapoints']:
            hour = datapoint['timestamp']
            hour = hour.strftime('%d%H')
            try:
                hour_dicts[hour]['kmh'].append(datapoint['kmh'])
                hour_dicts[hour]['ms'].append(datapoint['ms'])
                hour_dicts[hour]['knots'].append(datapoint['knots'])
            except:
                pass

        for key, value in hour_dicts.items():

            DB['wind_history'].update(
                {
                    'module_uid': ObjectId(anemometer['module_uid']),
                    'range': 'day'
                },
                {
                    '$set': {
                        'module_uid': ObjectId(anemometer['module_uid']),
                        'range': 'day',
                        f'hours.{key}.timestamp' : value['timestamp'],
                        f'hours.{key}.time' : value['time'],
                        f'hours.{key}.kmh' : value['kmh'],
                        f'hours.{key}.ms' : value['ms'],
                        f'hours.{key}.knots' : value['knots']
                    }
                },
                upsert=True
            )


def averageData(DB):

    hour_data = DB['wind_history'].find(
        {
            'range': 'day'
        }
    )

    for anemometer in hour_data:

        datapoints = []


        for key, value in anemometer['hours'].items():
            data = {}
            
            kmh_avg = []
            kmh_max = []
            kmh_min = []

            ms_avg = []
            ms_max = []
            ms_min = []
        
            knots_avg = []
            knots_max = []
            knots_min = []

            timestamp = value['timestamp']
            time = value['time']

            if len(value['kmh']) > 0:
                for kmh in value['kmh']:
                    kmh_avg.append(kmh['avg'])
                    kmh_max.append(kmh['max'])
                    kmh_min.append(kmh['min'])

                for ms in value['ms']:
                    ms_avg.append(ms['avg'])
                    ms_max.append(ms['max'])
                    ms_min.append(ms['min'])
                
                for knots in value['knots']:
                    knots_avg.append(knots['avg'])
                    knots_max.append(knots['max'])
                    knots_min.append(knots['min'])
                
                kmh_avg_hour = avg(kmh_avg)
                kmh_max_hour = max(kmh_max)
                kmh_min_hour = min(kmh_min)

                ms_avg_hour = avg(ms_avg)
                ms_max_hour = max(ms_max)
                ms_min_hour = min(ms_min)

                knots_avg_hour = avg(knots_avg)
                knots_max_hour = max(knots_max)
                knots_min_hour = min(knots_min)
            
            else:
                kmh_avg_hour = 0
                kmh_max_hour = 0
                kmh_min_hour = 0

                ms_avg_hour = 0
                ms_max_hour = 0
                ms_min_hour = 0

                knots_avg_hour = 0
                knots_max_hour = 0
                knots_min_hour = 0

            data['timestamp'] = timestamp
            data['time'] = time
            data['kmh'] = {
                'min' : kmh_min_hour,
                'avg' : kmh_avg_hour,
                'max' : kmh_max_hour
            }
            data['ms'] = {
                'min' : ms_min_hour,
                'avg' : ms_avg_hour,
                'max' : ms_max_hour
            }
            data['knots'] = {
                'min' : knots_min_hour,
                'avg' : knots_avg_hour,
                'max' : knots_max_hour
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
    time_day = time_now - datetime.timedelta(hours=24)

    anemometers = DB['wind_history'].find(
        {
            'range' : 'day'
        }
    )

    for anemometer in anemometers:
        purged_hours = {}

        hours = anemometer['hours']

        for key, value in hours.items():
            if value['timestamp'] > time_day:
                purged_hours[key] = value

        DB['wind_history'].find_one_and_update(
            {
                'range': 'day',
                'module_uid' : anemometer['module_uid']
            },
            {
                '$set' : {
                    'hours' : purged_hours
                }
            }
        )


def process(DB):

    hours = getHours(DB)
    hour_dicts = genHourList()
    formatData(DB, hours, hour_dicts)
    averageData(DB)
    purge(DB)
