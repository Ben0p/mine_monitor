
from env.sol import env

import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
import datetime
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
    database=f"{env['tetra_sql_database']}"
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

    print("Processing data..")

    for row in data:

        location = {}

        hex_string = row[5].hex()
        hex_string = hex_string.rstrip("0")
        try:
            location = copy.deepcopy(sds(str(hex_string)))
        except (ValueError, KeyError):
            # TODO fix some of those erros within the teta sds module
            continue

        timestamp = row[0]
        timestamp = timestamp.isoformat() + 'Z'

        
        lat = location['location']['latitude']['decimal_degrees']
        lon = location['location']['longitude']['decimal_degrees']
        alt = location['location']['altitude']['meters']

        lat, lon, alt = geodetic_to_geocentric(lat, lon, alt)

        point = [timestamp, lat, lon, alt]

        DB['map_tetra'].find_one_and_update(
            {
                'timestamp' : timestamp,
                'issi' : row[6]
            },
            {
                '$set' : {
                    'unix' : time.time(),
                    'issi' : row[6],
                    'type' : 'subscriber',
                    'timestamp' : timestamp,
                    'point' : point,
                    'uncertainty' : location['location']['uncertainty'],
                    'velocity' : location['velocity']['kmh'],
                    'direction' : location['direction']['direction'],
                    'angle' : location['direction']['angle']
                }
            },
            upsert=True
        )
    print("Finished processing data.")


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


def main():

    # Do initial data sync (30min)
    '''
    start = time.time()
    processData(getSDS(1800))
    end = time.time()
    total = round(end - start, 2)
    print(f"{datetime.datetime.now()} - Retrieved last 30min of SDS data in {total}s")
    '''
    # Get specific time range
    start = time.time()
    processData(getTimeRange('2020-06-21 18:00:00', '2020-06-21 20:00:00'))
    end = time.time()
    total = round(end - start, 2)
    print(f"{datetime.datetime.now()} - Retrieved range of SDS data in {total}s")

    # Polling interval (Seconds)
    interval = 60

    # Main loop
    while True:
        start = time.time()
        getSDS(interval)
        end = time.time()
        total = round(end - start, 2)
        print(f'{datetime.datetime.now()} - Polled SDS in {total}s')
        time.sleep(interval)




    


if __name__ == "__main__":

    main()
