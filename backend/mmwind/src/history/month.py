from env.sol import env

import datetime
import pytz
import pymongo
from bson import ObjectId


def getRange():

    # Get local time and make it timezone aware
    local_time = datetime.datetime.now()
    local_time = local_time.replace(tzinfo=pytz.timezone(env['timezone']))

    # Get the last hour
    last_day = local_time - datetime.timedelta(days=1)
    year = int(last_day.strftime('%Y'))
    month = int(last_day.strftime('%m'))
    day = int(last_day.strftime('%d'))

    day_timestamp = datetime.datetime(year, month, day)
    day_timestamp = day_timestamp.replace(tzinfo=pytz.timezone(env['timezone']))

    start = datetime.datetime(year, month, day, 0)
    start = start.replace(tzinfo=pytz.timezone(env['timezone']))

    end = datetime.datetime(year, month, day, 23)
    end = end.replace(tzinfo=pytz.timezone(env['timezone']))

    time = day_timestamp + datetime.timedelta(hours=env['local_offset'])
    time = time.strftime('%d/%m/%Y')

    day_str = day_timestamp + datetime.timedelta(hours=env['local_offset'])
    day_str = day_str.strftime('%Y%m%d')

    day_range = {
        'start' : start,
        'end' : end,
        'timestamp' : day_timestamp,
        'time' : time,
        'day' : day_str,
        'local_time' : local_time
    }

    return(day_range)


def getLastHour(DB, day_range):

    previous_days = []

    start = day_range['start']
    end = day_range['end']

    modules = DB['wind_modules'].find()

    for module in modules:

        previous_day = DB['wind_history'].find(
            {
                'module_uid' : module['_id'],
                'range' : 'day',
                'timestamp' :
                    {
                        '$lt': end,
                        '$gte': start
                    }

            }
        )
        previous_days.append(list(previous_day))
    return(previous_days)


def processHour(DB, last_days, day_range):

    averaged_days = []

    for last_day in last_days:
        try:
            kmh_max = max(d['kmh_max'] for d in last_day)
            kmh_avg = sum(d['kmh_avg'] for d in last_day) / len(last_day)
            kmh_avg = round(kmh_avg, 2)
            kmh_min = min(d['kmh_min'] for d in last_day)

            ms_max = max(d['ms_max'] for d in last_day)
            ms_avg = sum(d['ms_avg'] for d in last_day) / len(last_day)
            ms_avg = round(ms_avg, 2)
            ms_min = min(d['ms_min'] for d in last_day)

            knots_max = max(d['knots_max'] for d in last_day)
            knots_avg = sum(d['knots_avg'] for d in last_day) / len(last_day)
            knots_avg = round(knots_avg, 2)
            knots_min = min(d['knots_min'] for d in last_day)

            averaged_day = {
                'module_uid' : last_day[0]['module_uid'],
                'range' : 'month',
                'day' : day_range['day'],
                'time' : day_range['time'],
                'timestamp' : day_range['timestamp'],
                'kmh_max' : kmh_max,
                'kmh_avg' : kmh_avg,
                'kmh_min' : kmh_min,
                'ms_max' : ms_max,
                'ms_avg' : ms_avg,
                'ms_min' : ms_min,
                'knots_max' : knots_max,
                'knots_avg' : knots_avg,
                'knots_min' : knots_min
            }

            averaged_days.append(averaged_day)
 
        except ValueError:
            pass
        except IndexError:
            pass
    
    return(averaged_days)


def insertDB(DB, averaged_days):

    for day in averaged_days:
        DB['wind_history'].find_one_and_update(
            {
                'module_uid' : day['module_uid'],
                'range' : day['range'],
                'day' : day['day']
            },
            {
                '$set': {
                    'module_uid' : day['module_uid'],
                    'range' : day['range'],
                    'day' : day['day'],
                    'time' : day['time'],
                    'timestamp' : day['timestamp'],
                    'kmh_max' : day['kmh_max'],
                    'kmh_avg' : day['kmh_avg'],
                    'kmh_min' : day['kmh_min'],
                    'ms_max' : day['ms_max'],
                    'ms_avg' : day['ms_avg'],
                    'ms_min' : day['ms_min'],
                    'knots_max' : day['knots_max'],
                    'knots_avg' : day['knots_avg'],
                    'knots_min' : day['knots_min']
                }
            },
            upsert=True
        )


def purge(DB):
    ''' Purge older than 2 days
    '''
    local_time = datetime.datetime.now()
    local_time = local_time.replace(tzinfo=pytz.timezone(env['timezone']))

    DB['wind_history'].delete_many(
        {
            'range': 'month',
            'timestamp': {
                '$lte': local_time - datetime.timedelta(days=56)
            }
        },
    )


def process(DB):

    day_range = getRange()
    last_days = getLastHour(DB, day_range)
    averaged_days = processHour(DB, last_days, day_range)
    insertDB(DB, averaged_days)
    purge(DB)