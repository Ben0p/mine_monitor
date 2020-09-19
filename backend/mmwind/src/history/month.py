from env.sol import env

import datetime
import pymongo
from bson import ObjectId



def avg(speeds):

    average = sum(speeds) / len(speeds)
    average = round(average, 2)
    return(average)


def process(DB, uid):

    days = {}

    time_now = datetime.datetime.now()
    time_day = time_now - datetime.timedelta(days=28)

    speeds = DB['wind_data'].find(
        {
            'module_uid' : ObjectId(uid),
            'timestamp': {
                '$lt': time_now,
                '$gte': time_day
            }
        }
    ).sort("timestamp", pymongo.ASCENDING)

    speeds = list(speeds)


    module = DB['wind_modules'].find_one(
        {
            '_id' : ObjectId(uid)
        }
    )

    # Generate array of day dictionaries (28 days)
    for i in range(0,29,1):
        i = f'{i:02}'
        days[str(i)] = {
            'time' : [],
            'ms' : [],
            'kmh' : [],
            'knots' : []
        }

    for speed in speeds:
        day = speed['timestamp'].strftime('%d')

        days[day]['time'].append(speed['time'])
        days[day]['ms'].append(speed['ms'])
        days[day]['kmh'].append(speed['kmh'])
        days[day]['knots'].append(speed['knots'])

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

    # Get date times
    current_day = time_now.strftime('%d')
    current_day = int(current_day)
    start_month = speeds[0]['timestamp']
    start_month = start_month.strftime('%m')
    current_month = time_now.strftime('%m')
    year = time_now.strftime('%Y')

    for i in range(current_day,29,1):
        i = f'{i:02}'

        day = f"{i}/{start_month}/{year}"

        ms_speeds = days[i]['ms']
        kmh_speeds = days[i]['kmh']
        knots_speeds = days[i]['knots']
        times.append(day)

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
    
    for i in range(0,current_day,1):
        i = f'{i:02}'

        day = f"{i}/{current_month}/{year}"

        ms_speeds = days[i]['ms']
        kmh_speeds = days[i]['kmh']
        knots_speeds = days[i]['knots']
        times.append(day)

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
            'range': "month",
        },
        {
            '$set': {
                'module_uid': uid,
                'name' : module['name'],
                'range': "month",
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