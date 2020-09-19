from env.sol import env

import datetime
import pymongo
from bson import ObjectId



def avg(speeds):

    average = sum(speeds) / len(speeds)
    average = round(average, 2)
    return(average)


def process(DB, uid):

    hours = {}

    time_now = datetime.datetime.now()
    time_day = time_now - datetime.timedelta(hours=24)

    speeds = DB['wind_data'].find(
        {
            'module_uid' : ObjectId(uid),
            'timestamp': {
                '$lt': time_now,
                '$gte': time_day
            }
        }
    ).sort("timestamp", pymongo.DESCENDING)


    module = DB['wind_modules'].find_one(
        {
            '_id' : ObjectId(uid)
        }
    )

    # Generate array of minute dictionaries
    for i in range(0,24,1):
        i = f'{i:02}'
        hours[str(i)] = {
            'time' : [],
            'ms' : [],
            'kmh' : [],
            'knots' : []
        }

    for speed in speeds:
        hour = speed['timestamp'].strftime('%H')

        hours[hour]['time'].append(speed['time'])
        hours[hour]['ms'].append(speed['ms'])
        hours[hour]['kmh'].append(speed['kmh'])
        hours[hour]['knots'].append(speed['knots'])

    times = []

    ms_max = []
    ms_min = []
    ms_avg = []

    kmh_max = []
    kmh_min = []
    kmh_avg = []

    knots_max = []
    knots_min = []
    knots_avg = []

    current_hour = time_now.strftime('%H')
    current_hour = int(current_hour)

    for i in range(current_hour,24,1):
        i = f'{i:02}'

        # Set day to yesterday
        day = time_now - datetime.timedelta(hours=24)
        day = day.strftime('%d')
        date = time_now.strftime('%m/%Y')
        hour = f"{day}/{date} {i}:00"

        ms_speeds = hours[i]['ms']
        kmh_speeds = hours[i]['kmh']
        knots_speeds = hours[i]['knots']
        times.append(hour)

        if len(ms_speeds) >= 1:
            # m/s
            ms_max.append(max(ms_speeds))
            ms_min.append(min(ms_speeds))
            ms_avg.append(avg(ms_speeds))
            # km/h
            kmh_max.append(max(kmh_speeds))
            kmh_min.append(min(kmh_speeds))
            kmh_avg.append(avg(kmh_speeds))
            # Knots
            knots_max.append(max(knots_speeds))
            knots_min.append(min(knots_speeds))
            knots_avg.append(avg(knots_speeds))
        else:
            # m/s
            ms_max.append(0)
            ms_min.append(0)
            ms_avg.append(0)
            # km/h
            kmh_max.append(0)
            kmh_min.append(0)
            kmh_avg.append(0)
            # Knots
            knots_max.append(0)
            knots_min.append(0)
            knots_avg.append(0)
    
    for i in range(0,current_hour,1):
        i = f'{i:02}'

        # Set day to today
        day = time_now
        day = day.strftime('%d')
        date = time_now.strftime('%m/%Y')
        hour = f"{day}/{date} {i}:00"

        ms_speeds = hours[i]['ms']
        kmh_speeds = hours[i]['kmh']
        knots_speeds = hours[i]['knots']
        times.append(hour)

        if len(ms_speeds) >= 1:
            # m/s
            ms_max.append(max(ms_speeds))
            ms_min.append(min(ms_speeds))
            ms_avg.append(avg(ms_speeds))
            # km/h
            kmh_max.append(max(kmh_speeds))
            kmh_min.append(min(kmh_speeds))
            kmh_avg.append(avg(kmh_speeds))
            # Knots
            knots_max.append(max(knots_speeds))
            knots_min.append(min(knots_speeds))
            knots_avg.append(avg(knots_speeds))
        else:
            # m/s
            ms_max.append(0)
            ms_min.append(0)
            ms_avg.append(0)
            # km/h
            kmh_max.append(0)
            kmh_min.append(0)
            kmh_avg.append(0)
            # Knots
            knots_max.append(0)
            knots_min.append(0)
            knots_avg.append(0)
    
    DB['wind_history'].find_one_and_update(
        {
            'module_uid': uid,
            'range': "day",
        },
        {
            '$set': {
                'module_uid': uid,
                'name' : module['name'],
                'range': "day",
                'time': times,
                'ms': {
                    'max': ms_max,
                    'min': ms_min,
                    'avg': ms_avg
                },
                'kmh': {
                    'max': kmh_max,
                    'min': kmh_min,
                    'avg': kmh_avg
                },
                'knots': {
                    'max': knots_max,
                    'min': knots_min,
                    'avg': knots_avg
                }
            }
        },
        upsert=True
    )