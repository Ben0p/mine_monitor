from env.sol import env

import datetime
import pymongo
from bson import ObjectId
import time


def getRange():

    # Get the seconds range of the last mintute from now
    last_minute = datetime.datetime.now() - datetime.timedelta(minutes=1)
    year = int(last_minute.strftime('%Y'))
    month = int(last_minute.strftime('%m'))
    day = int(last_minute.strftime('%d'))
    hour = int(last_minute.strftime('%H'))
    minute = int(last_minute.strftime('%M'))
    minute_timestamp = datetime.datetime(year, month, day, hour, minute)
    start = datetime.datetime(year, month, day, hour, minute, 00)
    end = datetime.datetime(year, month, day, hour, minute, 59)
    time = minute_timestamp.strftime('%d/%m/%Y %H:%M')
    unix = minute_timestamp.timestamp()
    minute_str = minute_timestamp.strftime('%Y%m%d%H%M')

    minute_range = {
        'start' : start,
        'end' : end,
        'timestamp' : minute_timestamp,
        'time' : time,
        'minute' : minute_str,
        'unix' : unix
    }

    return(minute_range)


def getLastMinute(DB, minute_range):

    previous_minutes = []

    start = minute_range['start']
    end = minute_range['end']

    modules = DB['wind_modules'].find()

    for module in modules:

        previous_minute = DB['wind_history'].find(
            {
                'module_uid' : module['_id'],
                'range' : 'minute',
                'timestamp' :
                    {
                        '$lt': end,
                        '$gte': start
                    }

            }
        )
        previous_minutes.append(list(previous_minute))
    return(previous_minutes)


def processMinute(DB, last_minutes, minute_range):

    averaged_minutes = []

    for last_minute in last_minutes:
        try:
            kmh_max = max(d['kmh'] for d in last_minute)
            kmh_avg = sum(d['kmh'] for d in last_minute) / len(last_minute)
            kmh_avg = round(kmh_avg, 2)
            kmh_min = min(d['kmh'] for d in last_minute)

            ms_max = max(d['ms'] for d in last_minute)
            ms_avg = sum(d['ms'] for d in last_minute) / len(last_minute)
            ms_avg = round(ms_avg, 2)
            ms_min = min(d['ms'] for d in last_minute)

            knots_max = max(d['knots'] for d in last_minute)
            knots_avg = sum(d['knots'] for d in last_minute) / len(last_minute)
            knots_avg = round(knots_avg, 2)
            knots_min = min(d['knots'] for d in last_minute)

            averaged_minute = {
                'module_uid' : last_minute[0]['module_uid'],
                'range' : 'hour',
                'minute' : minute_range['minute'],
                'time' : minute_range['time'],
                'timestamp' : minute_range['timestamp'],
                'unix' : minute_range['unix'],
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

            averaged_minutes.append(averaged_minute)
 
        except ValueError:
            pass
        except IndexError:
            pass
    
    return(averaged_minutes)


def insertDB(DB, averaged_minutes):

    for minute in averaged_minutes:
        DB['wind_history'].find_one_and_update(
            {
                'module_uid' : minute['module_uid'],
                'range' : minute['range'],
                'minute' : minute['minute']
            },
            {
                '$set': {
                    'module_uid' : minute['module_uid'],
                    'range' : minute['range'],
                    'minute' : minute['minute'],
                    'time' : minute['time'],
                    'timestamp' : minute['timestamp'],
                    'unix' : minute['unix'],
                    'kmh_max' : minute['kmh_max'],
                    'kmh_avg' : minute['kmh_avg'],
                    'kmh_min' : minute['kmh_min'],
                    'ms_max' : minute['ms_max'],
                    'ms_avg' : minute['ms_avg'],
                    'ms_min' : minute['ms_min'],
                    'knots_max' : minute['knots_max'],
                    'knots_avg' : minute['knots_avg'],
                    'knots_min' : minute['knots_min']
                }
            },
            upsert=True
        )


def purge(DB):
    ''' Purge older than 2 hours
    '''

    DB['wind_history'].delete_many(
        {
            'range': 'hour',
            'unix': {
                '$lte': time.time() - 7200
            }
        },
    )


def process(DB):

    minute_range = getRange()
    last_minutes = getLastMinute(DB, minute_range)
    averaged_minutes = processMinute(DB, last_minutes, minute_range)
    insertDB(DB, averaged_minutes)
    purge(DB)
