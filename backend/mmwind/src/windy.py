from env.sol import env

import pymssql
import json
import pymongo
import datetime
import time

# Initialize mongo
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]

# Initialize SQL
conn = pymssql.connect(
    server = env['pcs_sql_server'],
    user = f"{env['pcs_sql_domain']}\\{env['pcs_sql_username']}",
    password = env['pcs_sql_password']
)

cursor = conn.cursor()

def poll_anemometers():
    ''' Does the SQL query and parses json data 
    '''

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
            ms = float(value[0]['V'])
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
                datapoint_time = datapoint_time.strftime('%d/%m/%Y %H:%M:%S')
                
                print(f"    {datapoint_time} - {datapoint['V']} m/s")
            
            # Insert into mongo DB
            DB['pcs_wind'].find_one_and_update(
                        {
                            'name' : location,
                        },
                        {
                            '$set': {
                                'name': location,
                                'timestamp' : timestamp,
                                'time' : time_string,
                                'ms' : ms,
                                'kmh' : kmh,
                                'knots' : knots
                            }
                        },
                        upsert=True
                    )




if __name__ == "__main__":

    while True:
        poll_anemometers()

        time.sleep(10)