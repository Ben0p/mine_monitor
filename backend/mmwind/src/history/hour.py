from env.sol import env

import datetime
import pymongo
from bson import ObjectId


def avg(speeds):

    average = sum(speeds) / len(speeds)
    average = round(average, 2)
    return(average)


def process(DB, uid):

    minutes = {}

    time_now = datetime.datetime.now()
    time_hour = time_now - datetime.timedelta(hours=1)

    speeds = DB['wind_data'].find(
        {
            'module_uid': ObjectId(uid),
            'timestamp': {
                '$lt': time_now,
                '$gte': time_hour
            }
        }
    ).sort("timestamp", pymongo.DESCENDING)

    module = DB['wind_modules'].find_one(
        {
            '_id' : ObjectId(uid)
        }
    )

    # Generate array of minute dictionaries
    for i in range(0, 60, 1):
        i = f'{i:02}'
        minutes[str(i)] = {
            'time': [],
            'ms': [],
            'kmh': [],
            'knots': []
        }

    for speed in speeds:
        minute = speed['timestamp'].strftime('%M')

        minutes[minute]['time'].append(speed['time'])
        minutes[minute]['ms'].append(speed['ms'])
        minutes[minute]['kmh'].append(speed['kmh'])
        minutes[minute]['knots'].append(speed['knots'])

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

    current_minute = time_now.strftime('%M')
    current_minute = int(current_minute)

    for i in range(current_minute+1, 60, 1):
        # Starting at current minute 0 padded
        i = f'{i:02}'

        # Set hour to last hour
        hour = time_now - datetime.timedelta(hours=1)
        hour = hour.strftime('%H')
        date = time_now.strftime('%d/%m/%Y')
        minute = f"{date} {hour}:{i}"

        ms_speeds = minutes[i]['ms']
        kmh_speeds = minutes[i]['kmh']
        knots_speeds = minutes[i]['knots']
        times.append(minute)

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

    for i in range(0, current_minute, 1):
        i = f'{i:02}'

        # Set hour to current hour
        hour = time_now
        hour = hour.strftime('%H')
        date = time_now.strftime('%d/%m/%Y')
        minute = f"{date} {hour}:{i}"

        ms_speeds = minutes[i]['ms']
        kmh_speeds = minutes[i]['kmh']
        knots_speeds = minutes[i]['knots']
        times.append(minute)

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
            'range': "hour"
        },
        {
            '$set': {
                'module_uid': uid,
                'name' : module['name'],
                'range': "hour",
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
