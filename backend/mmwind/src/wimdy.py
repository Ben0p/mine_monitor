from env.sol import env

import pyodbc
import json
import datetime
import pymongo
from bson import ObjectId
import time
import pytz
from subprocess import Popen, PIPE, TimeoutExpired

from history import minute, hour, day, month



# Initialize mongo
CLIENT = pymongo.MongoClient(
    f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}")
DB = CLIENT[env['database']]

def kerberos():

    '''
    password = "5U!Y7$gaxS!NVnO78l$c"

    kinit = '/usr/bin/kinit'
    kinit_args = [ kinit, 'svc.solmm' ]
    kinit = Popen(kinit_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    kinit.stdin.write(f'{password}\n'.encode())
    '''
    pass


def connectSQL():
    ''' Connects to SQL
    '''

    driver = '{ODBC Driver 17 for SQL Server}'

    cnxn = pyodbc.connect(
        f"Trusted_connection=yes; \
        DRIVER={driver}; \
        KERBEROS=True; \
        SERVER=SOLOPSRS02.fmg.local;")

    cursor = cnxn.cursor()
    return(cursor)


def pollSQL(cursor):
    if cursor:
        # SQL Query
        cursor.execute("SELECT top 1 \
            [Timestamp], \
            [Subscriber], \
            [Data] \
            FROM [SOLOPFReports].[PCS].[DataPublish] \
            where Subscriber = 'solmm01' \
            order by Timestamp desc")
        rows = cursor.fetchall()
        return(rows)
    else:
        return(False)


def insertOffline():
    ''' Inserts offline data into mongo
    '''

    modules = DB['wind_modules'].find()

    for module in modules:

        DB['wind_live'].find_one_and_update(
            {
                'module_uid': module['_id'],
            },
            {
                '$set': {
                    'module_uid' : module['_id'],
                    'online' : False,
                    'status' : 'primary',
                    'speed' : 'stop'
                }
            },
            upsert=True
        )


def processData(rows):
    ''' Processes data in each row returned by the SQL query
        Returns processed dictionary array
    '''
    # Iterate rows (should only be one anyway)
    for row in rows:

        # Get time object and format it
        timestamp = row[0]
        # Make timezone aware
        timestamp = timestamp.replace(tzinfo=pytz.timezone(env['timezone']))
        time_string = timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print("-"*32)
        print(f"Time Stamp: {time_string}")
        print("-"*32)

        # Load json data
        data = json.loads(row[2])

        # Reset results
        results = {}

        # Iterate over aneometers in json (dictionary) object
        for key, value in data.items():

            module = DB['wind_modules'].find_one(
                {
                    'tag': key,
                }
            )

            if module:

                # Create module dictionary in the results dictionary
                # Also resets it for next module iteration
                module_uid = str(module['_id'])
                results[module_uid] = {}
                results[module_uid]['datapoints'] = []

                # Check speed units
                if module['units'] == 'ms':
                    # Speed unit conversions
                    ms = float(value[-1]['V'])
                    kmh = ms * 3.6
                    kmh = round(kmh, 2)
                    knots = ms * 1.944
                    knots = round(knots, 2)

                # Print out the name
                print(f"{module['name']}:")
                # Iterate datapoints in the value
                for datapoint in value:
                    try:
                        # If there is milliseconds
                        datapoint_time = datetime.datetime.strptime(
                            datapoint['T'], '%Y-%m-%dT%H:%M:%S.%f')
                    except ValueError:
                        # If there is no milliseconds
                        datapoint_time = datetime.datetime.strptime(
                            datapoint['T'], '%Y-%m-%dT%H:%M:%S')

                    # Make timezone aware
                    datapoint_time = datapoint_time.replace(tzinfo=pytz.timezone('Etc/GMT+0'))

                    # Add time offset and format to readable string
                    local_time = datetime.datetime.now()
                    local_time = local_time.replace(tzinfo=pytz.timezone(env['timezone']))

                    # Time String
                    datapoint_time_string = datapoint_time + datetime.timedelta(hours=8)
                    datapoint_time_string = datapoint_time_string.strftime('%d/%m/%Y %H:%M:%S')

                    # Process the speed status
                    if kmh <= 20:
                        speed = 'slow'
                        status = 'success'
                    elif 20 < kmh <= 40:
                        speed = 'medium'
                        status = 'warning'
                    elif 40 < kmh:
                        speed = 'fast'
                        status = 'danger'

                    # Offline if time stamp is older than 30sec
                    if datapoint_time  < local_time - datetime.timedelta(seconds=30):
                        online = False
                        speed = 'stop'
                        status = 'primary'
                    else:
                        online = True

                    # Print the result
                    print(f"    {datapoint_time_string} - {datapoint['V']} m/s")

                    # Construct dictionary of values
                    anemometer = {
                        'timestamp': datapoint_time,
                        'time': datapoint_time_string,
                        'ms': ms,
                        'kmh': kmh,
                        'knots': knots,
                        'online': online,
                        'speed': speed,
                        'status': status,
                    }

                    # Append results to dictionary of anemometer uids
                    results[module_uid]['datapoints'].append(anemometer)

    return(results)


def getLatest(anemometers):
    ''' Takes list of processed anemometer data
        Returns most recent data point for each anemometer
    '''

    latest = []

    # Get uid and data
    for key, value in anemometers.items():
        # Get last item in datapoints list
        # (always in order from SQL)
        latest_data = value['datapoints'][-1]
        latest_data['module_uid'] = ObjectId(key)

        # Append to latest list
        latest.append(latest_data)

    return(latest)


def insertLive(anemometers):
    ''' Takes array of anemometer dictionaries
        Inserts each anemometer dictionary into MongoDB collection
    '''
    
    for anemometer in anemometers:
        # Insert into mongo DB
        DB['wind_live'].find_one_and_update(
            {
                'module_uid': anemometer['module_uid'],
            },
            {
                '$set': {
                    'module_uid' : anemometer['module_uid'],
                    'timestamp' : anemometer['timestamp'],
                    'time' : anemometer['time'],
                    'ms' : anemometer['ms'],
                    'kmh' : anemometer['kmh'],
                    'knots' : anemometer['knots'],
                    'online' : anemometer['online'],
                    'speed' : anemometer['speed'],
                    'status' : anemometer['status']
                }
            },
            upsert=True
        )


def run():
    ''' Main run loop
    '''

   
    while True:
        kerberos()
        cursor = connectSQL()
        # Get data from SQL
        
        if cursor:
            while True:
                try:
                    rows = pollSQL(cursor)
                except:
                    break
        
                if rows:
                    # Process data
                    anemometers = processData(rows)
                    # Get most recent time stamp
                    latest = getLatest(anemometers)
                    # Insert live data 
                    insertLive(latest)
                    # Process current minute
                    minute.process(DB, anemometers)
                    # Process current hour
                    hour.process(DB)
                    # Process current day
                    day.process(DB)
                    # Process current month
                    month.process(DB)

                time.sleep(5)
        else:
            insertOffline()
            time.sleep(30)



if __name__ == "__main__":

    run()
