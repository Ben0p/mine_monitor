from env.sol import env

import pyodbc
import json
import datetime
import time
import pymongo

# Initialize mongo
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}")
DB = CLIENT[env['database']]


# Initialize SQL (Docker pyodbc)

driver = "{ODBC Driver 17 for SQL Server}"
server = 'SOLOPSRS02' 
username = 'FMG\\svc.sol.wind' 
password = '5U!Y7$gaxS!NVnO78l$c' 

cnxn = pyodbc.connect(f'DRIVER={driver}; \
    SERVER=SOLOPSRS02; \
    UID={username}; \
    PWD={password}; \
    Trusted_connection=yes')

cursor = cnxn.cursor()


def poll_anemometers():


    # SQL Query
    cursor.execute("SELECT top 1 \
        [Timestamp], \
        [Subscriber], \
        [Data] \
        FROM [SOLOPFReports].[PCS].[DataPublish] \
        where Subscriber = 'solmm01' \
        order by Timestamp desc")  
    rows = cursor.fetchall()

    # Iterate rows (should only be one anyway)
    for row in rows:

        # Get time object and format it
        timestamp = row[0]
        time_string = timestamp.strftime('%d/%m/%Y %H:%M:%S')
        print("-"*30)
        print(f"Time Stamp: {time_string}")
        print("-"*30)

        # Load json data
        data = json.loads(row[2])

        # Iterate over aneometers in json (dictionary) object
        for key, value in data.items():

            # Strip just the first part of the name
            location = key.split(".")[0]

            # Speed unit conversions
            ms = float(value[-1]['V'])
            kmh = ms * 3.6
            kmh = round(kmh, 2)
            knots = ms * 1.944
            knots = round(knots,2)

            # Print out the data points (for each unit)
            print(f"{location}:")
            for datapoint in value:
                try:
                    datapoint_time = datetime.datetime.strptime(datapoint['T'], '%Y-%m-%dT%H:%M:%S.%f')
                except ValueError:
                    datapoint_time = datetime.datetime.strptime(datapoint['T'], '%Y-%m-%dT%H:%M:%S')

                # Add time offset and format to readable string
                datapoint_time = datapoint_time + datetime.timedelta(hours=env['time_offset'])
                datapoint_time_string = datapoint_time.strftime('%d/%m/%Y %H:%M:%S')

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
                if datapoint_time < datetime.datetime.fromtimestamp(time.time() - 30):
                    online = False
                    speed = 'stop'
                    status = 'primary'
                else:
                    online = True

                
                print(f"    {datapoint_time} - {datapoint['V']} m/s")

            
            # Insert into mongo DB

            DB['wind_live'].find_one_and_update(
                        {
                            'name' : location,
                        },
                        {
                            '$set': {
                                'type' : "speed",
                                'name': location,
                                'timestamp' : datapoint_time,
                                'time' : datapoint_time_string,
                                'ms' : ms,
                                'kmh' : kmh,
                                'knots' : knots,
                                'online' : online,
                                'speed' : speed,
                                'status' : status,
                            }
                        },
                        upsert=True
                    )



if __name__ == "__main__":

    while True:
        poll_anemometers()

        time.sleep(10)