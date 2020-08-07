
from env.sol import env

import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
import datetime
from datetime import timedelta
from pytz import timezone
import mysql.connector
import math

from tetra.decode import sds


# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]


def reconnectSQL():
    # Initialize mySQL connection
    sql = mysql.connector.connect(
    host=f"{env['tetra_sql_host']}",
    user=f"{env['tetra_sql_user']}",
    passwd=f"{env['tetra_sql_passwd']}",
    database=f"{env['tetra_sql_database']}",
    autocommit=True
    )

    return(sql)


def geodetic_to_geocentric(lat, lon, h):
    """
    Compute the Geocentric (Cartesian) Coordinates X, Y, Z
    given the Geodetic Coordinates lat, lon + Ellipsoid Height h
    """

    ## Ellipsoid Parameters as tuples (semi major axis, inverse flattening)
    grs80 = (6378137, 298.257222100882711)
    wgs84 = (6378137, 298.257223563)
    a, rf = wgs84
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    N = a / math.sqrt(1 - (1 - (1 - 1 / rf) ** 2) * (math.sin(lat_rad)) ** 2)
    X = (N + h) * math.cos(lat_rad) * math.cos(lon_rad)
    Y = (N + h) * math.cos(lat_rad) * math.sin(lon_rad)
    Z = ((1 - 1 / rf) ** 2 * N + h) * math.sin(lat_rad)

    return(X, Y, Z)


def processData(data):

    start_process_time = time.time()

    # Get subscriber list from mongo
    subs = DB['tetra_subscribers'].find()
    sub_list = {sub['ssi'] : sub for sub in subs}

    generate_sub_dictionary = time.time()
    gen_sub_time = round(generate_sub_dictionary - start_process_time,2)
    print(f"Generate subscriber list...........{gen_sub_time}s")


    for row in data:

        location = {}

        # Process raw binary into location data
        hex_string = row[5].hex()
        hex_string = hex_string.rstrip("0")
        try:
            location = copy.deepcopy(sds(str(hex_string)))
        except (ValueError, KeyError):
            # TODO fix some of those erros within the teta sds module
            continue

        # Convert lat, lon into geocentric
        # TODO incorporate into SDS module
        lat = location['location']['latitude']['decimal_degrees']
        lon = location['location']['longitude']['decimal_degrees']
        alt = location['location']['altitude']['meters']
        lat, lon, alt = geodetic_to_geocentric(lat, lon, alt)

        # MySQL timestamp
        timestamp = row[0]
        timestamp = timestamp.isoformat()
        timestamp = timestamp + 'Z'

        # Availability start time
        availability_start = row[0]
        availability_start = availability_start + timedelta(minutes=-30)
        availability_start = availability_start.isoformat()
        availability_start = availability_start + 'Z'  

        # Availability finish time
        availability_end = row[0]
        availability_end = availability_end + timedelta(minutes=1)
        availability_end = availability_end.isoformat()
        availability_end = availability_end + 'Z'

        # Properties start time
        properties_start = row[0]
        properties_start = properties_start + timedelta(minutes=-1)
        properties_start = properties_start.isoformat()
        properties_start = properties_start + 'Z'  

        # Properties end time
        properties_end = row[0]
        properties_end = properties_end + timedelta(minutes=15)
        properties_end = properties_end.isoformat()
        properties_end = properties_end + 'Z'

        

     

        # Combine into timestamped point
        point = [timestamp, lat, lon, alt]

        # Test key values
        try:
            sub_list[row[6]]['description']
        except KeyError:
            sub_list[row[6]]['description'] = ''
        try:
            sub_list[row[6]]['node']
        except KeyError:
            sub_list[row[6]]['node'] = ''
        try:
            sub_list[row[6]]['talkgroup']
        except KeyError:
            sub_list[row[6]]['talkgroup'] = ''

        # Process RSSI
        if row[3] >= -70:
            rssi_color = [63, 191, 63, 128]
        elif -70 > row[3] >= -90:
            rssi_color = [191, 178, 63, 128]
        elif -90 > row[3]:
            rssi_color = [191, 63, 63, 128]

        # Process speed
        if location['velocity']['kmh'] > 60:
            velocity_color = [191, 63, 63, 128]
        else:
            velocity_color = [63, 191, 63, 128]

            
        # Insert into Mongo
        DB['sds_data'].insert_one(
            {
                    'unix' : time.time(),
                    'issi' : row[6],
                    'description' : sub_list[row[6]]['description'],
                    'node' : sub_list[row[6]]['node'],
                    'talkgroup': sub_list[row[6]]['talkgroup'],
                    'type' : 'subscriber',
                    'timestamp' : timestamp,
                    'processed_time' : datetime.datetime.utcnow(),
                    'availability_start' : availability_start,
                    'availability_end' : availability_end,
                    'properties_start' : properties_start,
                    'properties_end' : properties_end,
                    'point' : point,
                    'rssi' : row[3],
                    'rssi_color' : rssi_color,
                    'uncertainty' : location['location']['uncertainty'],
                    'velocity' : location['velocity']['kmh'],
                    'velocity_color' : velocity_color,
                    'direction' : location['direction']['direction'],
                    'angle' : location['direction']['angle']
            },
        )
    finish_process_time = time.time()
    insert_mongo = round(finish_process_time - generate_sub_dictionary, 2)
    print(f"Process SDS data and update DB.....{insert_mongo}s")



def getSDS(interval):

    sql = reconnectSQL()
    cursor = sql.cursor()

    # Execute MySQL query
    cursor.execute(f"SELECT \
        Timestamp, \
        OriginatingNodeNo, \
        UserDataLength, \
        Rssi, \
        MsDistance, \
        UserData, \
        CallingSsi \
        FROM sdsdata \
        WHERE UserDataLength = 129 \
        AND Timestamp > date_sub(now(), interval {28800 + interval} second) \
        ORDER BY Timestamp ASC"
    )

    myresult = cursor.fetchall()
    cursor.close()

    return(myresult)


def getTimeRange(start, end):

    sql = reconnectSQL()
    cursor = sql.cursor()

    # Execute MySQL query
    cursor.execute(f"SELECT \
        Timestamp, \
        OriginatingNodeNo, \
        UserDataLength, \
        Rssi, \
        MsDistance, \
        UserData, \
        CallingSsi \
        FROM sdsdata \
        WHERE UserDataLength = 129 \
        AND Timestamp between '{start}' and '{end}' \
        ORDER BY Timestamp ASC"
    )

    print("Destroying MySQL...")
    start = time.time()
    myresult = cursor.fetchall()
    end = time.time()
    print(f"Query took {end-start} seconds")

    return(myresult)

def truncate_data(seconds):
    ''' Delete SDS data older than 1 week
    '''

    DB['sds_data'].delete_many(
        {
            'unix' : {
                '$lte' : time.time() - seconds
            }
        },
    )


def main():


    # Main loop
    while True:
        print('-'*40)
        print(datetime.datetime.now())
        print('-'*40)
        start = time.time()

        data = getSDS(60)

        finish_data = time.time()
        get_data_time = round(finish_data - start, 2)
        print(f"Get raw sds data...................{get_data_time}s")

        processData(data)

        truncate_start = time.time()
        truncate_data(604800)
        truncate_finish = time.time()
        truncate_total = round(truncate_finish - truncate_start, 2)
        print(f'Trunkate SDS data..................{truncate_total}s')

        end = time.time()
        total = round(end - start, 2)
        print(f'Total..............................{total}s')

        time.sleep(30)




    


if __name__ == "__main__":

    main()
