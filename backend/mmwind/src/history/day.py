from env.sol import env

import datetime
import pymongo
from bson import ObjectId


def getRange():

    # Get the seconds range of the last hour from now
    local_time = datetime.datetime.now() + datetime.timedelta(hours=env['local_offset'])

    last_hour = local_time - datetime.timedelta(hours=1)
    year = int(last_hour.strftime('%Y'))
    month = int(last_hour.strftime('%m'))
    day = int(last_hour.strftime('%d'))
    hour = int(last_hour.strftime('%H'))
    hour_timestamp = datetime.datetime(year, month, day, hour)
    start = datetime.datetime(year, month, day, hour, 0)
    end = datetime.datetime(year, month, day, hour, 59)
    time = hour_timestamp.strftime('%d/%m/%Y %H:00')
    hour_str = hour_timestamp.strftime('%Y%m%d%H%M')

    hour_range = {
        'start' : start,
        'end' : end,
        'timestamp' : hour_timestamp,
        'time' : time,
        'hour' : hour_str,
        'local_time' : local_time
    }

    return(hour_range)


def getLastHour(DB, hour_range):

    previous_hours = []

    start = hour_range['start']
    end = hour_range['end']

    modules = DB['wind_modules'].find()

    for module in modules:

        previous_hour = DB['wind_history'].find(
            {
                'module_uid' : module['_id'],
                'range' : 'hour',
                'timestamp' :
                    {
                        '$lt': end,
                        '$gte': start
                    }

            }
        )
        previous_hours.append(list(previous_hour))
    return(previous_hours)


def processHour(DB, last_hours, hour_range):

    averaged_hours = []

    for last_hour in last_hours:
        try:
            kmh_max = max(d['kmh_max'] for d in last_hour)
            kmh_avg = sum(d['kmh_avg'] for d in last_hour) / len(last_hour)
            kmh_avg = round(kmh_avg, 2)
            kmh_min = min(d['kmh_min'] for d in last_hour)

            ms_max = max(d['ms_max'] for d in last_hour)
            ms_avg = sum(d['ms_avg'] for d in last_hour) / len(last_hour)
            ms_avg = round(ms_avg, 2)
            ms_min = min(d['ms_min'] for d in last_hour)

            knots_max = max(d['knots_max'] for d in last_hour)
            knots_avg = sum(d['knots_avg'] for d in last_hour) / len(last_hour)
            knots_avg = round(knots_avg, 2)
            knots_min = min(d['knots_min'] for d in last_hour)

            averaged_hour = {
                'module_uid' : last_hour[0]['module_uid'],
                'range' : 'day',
                'hour' : hour_range['hour'],
                'time' : hour_range['time'],
                'timestamp' : hour_range['timestamp'],
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

            averaged_hours.append(averaged_hour)
 
        except ValueError:
            pass
        except IndexError:
            pass
    
    return(averaged_hours)


def insertDB(DB, averaged_hours):

    for hour in averaged_hours:
        DB['wind_history'].find_one_and_update(
            {
                'module_uid' : hour['module_uid'],
                'range' : hour['range'],
                'hour' : hour['hour']
            },
            {
                '$set': {
                    'module_uid' : hour['module_uid'],
                    'range' : hour['range'],
                    'hour' : hour['hour'],
                    'time' : hour['time'],
                    'timestamp' : hour['timestamp'],
                    'kmh_max' : hour['kmh_max'],
                    'kmh_avg' : hour['kmh_avg'],
                    'kmh_min' : hour['kmh_min'],
                    'ms_max' : hour['ms_max'],
                    'ms_avg' : hour['ms_avg'],
                    'ms_min' : hour['ms_min'],
                    'knots_max' : hour['knots_max'],
                    'knots_avg' : hour['knots_avg'],
                    'knots_min' : hour['knots_min']
                }
            },
            upsert=True
        )


def purge(DB):
    ''' Purge older than 2 days
    '''
    local_time = datetime.datetime.now() + datetime.timedelta(hours=env['local_offset'])

    DB['wind_history'].delete_many(
        {
            'range': 'hour',
            'unix': {
                '$lte': local_time - datetime.timedelta(days=2)
            }
        },
    )


def process(DB):

    hour_range = getRange()
    last_hours = getLastHour(DB, hour_range)
    averaged_hours = processHour(DB, last_hours, hour_range)
    insertDB(DB, averaged_hours)
    purge(DB)