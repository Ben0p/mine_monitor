from env.sol import env

import time
import pymongo
from datetime import datetime, timedelta
import pytz


def windDirection(deg):
    deg = float(deg)
    direction = 'N'

    if deg >= 349 and deg <= 11:
        direction = 'N'
    elif deg >= 12 and deg <= 33:
        direction = 'NNE'
    elif deg >= 34 and deg <= 56:
        direction = 'NE'
    elif deg >= 57 and deg <= 78:
        direction = 'ENE'
    elif deg >= 79 and deg <= 101:
        direction = 'E'
    elif deg >= 102 and deg <= 123:
        direction = 'ESE'
    elif deg >= 124 and deg <= 146:
        direction = 'SE'
    elif deg >= 147 and deg <= 168:
        direction = 'SSE'
    elif deg >= 169 and deg <= 191:
        direction = 'S'
    elif deg >= 192 and deg <= 213:
        direction = 'SSW'
    elif deg >= 214 and deg <= 236:
        direction = 'SW'
    elif deg >= 237 and deg <= 258:
        direction = 'WSW'
    elif deg >= 259 and deg <= 281:
        direction = 'W'
    elif deg >= 282 and deg <= 303:
        direction = 'WNW'
    elif deg >= 304 and deg <= 326:
        direction = 'NW'
    elif deg >= 327 and deg <= 348:
        direction = 'NNW'

    return(direction)


def generate(DB):

    # Set default values
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE',
                  'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    speeds = []
    locations = []
    results = []
    direction_data = {}

    # Generate an array of 16x 0's for the 16 directions
    for direction in directions:
        direction_data[direction] = []

    # Get locations
    for location in DB['weather_data'].distinct('location',  {'type': 'Atmospheric'}):
        locations.append(location)

    # End date time (Yesterday 16:00 pm)
    end_timestamp = datetime.today() - timedelta(days=1)
    end_timestamp = end_timestamp.replace(
        hour=15, minute=59, second=59, microsecond=00)
    end_timestamp.replace(tzinfo=pytz.timezone('Etc/GMT-0'))
    # Start 24 hours before yesterday 16:00 pm
    start_timestamp = end_timestamp - timedelta(days=1)
    start_timestamp = start_timestamp.replace(
        hour=16, minute=00, second=00, microsecond=00)

    print(f"Start: {start_timestamp} Etc/GMT-0")
    print(f"  End: {end_timestamp} Etc/GMT-0")

    for location in locations:
        # Get the astmospheric data (contains wind)
        atmospherics = DB['weather_data'].find(
            {
                'type': 'Atmospheric',
                'timestamp': {
                    '$gte': start_timestamp,
                    '$lte': end_timestamp
                },
                'location': location
            }
        )

        # Iterate over data
        for atmos in atmospherics:
            # If there is direction data
            if atmos['WD (deg)']:
                # Reverse the direction 180 deg (for wind rose graphic)
                deg = float(atmos['WD (deg)'])
                if 0 <= deg <= 180:
                    deg = deg + 180
                elif 181 <= deg <= 360:
                    deg = deg - 180

                # Convert degrees into a direction
                direction = windDirection(deg)
                # Append speed to the direction dictionary
                direction_data[direction].append(float(atmos['WS (m/s)']))

                date = atmos['date']

        '''
        # Get the index of that direction
        index = directions.index(direction)
        # Insert wind speed into the index of the array for that direction
        speeds[index] = float(atmos['WS (m/s)'])
        '''

        speeds = {
            'max': [],
            'min': [],
            'avg': []
        }

        for key, value in direction_data.items():
            ms_max = 0
            ms_avg = 0
            ms_min = 0

            if len(value) > 0:
                ms_max = max(value)
                ms_avg = sum(value) / len(value)
                ms_avg = round(ms_avg, 2)
                ms_min = min(value)

            avg_offset = ms_avg - ms_min
            avg_offset = round(avg_offset, 2)
            max_offset = ms_max - ms_avg
            max_offset = round(max_offset, 2)

            speeds['max'].append(max_offset)
            speeds['avg'].append(avg_offset)
            speeds['min'].append(ms_min)

        result = {
            'location': location,
            'date': date,
            'speeds': speeds,
            'type': 'windrose'
        }

        DB['weather_charts'].find_one_and_update(
            {
                'date': date,
                'location': location,
                'type': 'windrose'
            },
            {
                '$set': result
            },
            upsert=True
        )
