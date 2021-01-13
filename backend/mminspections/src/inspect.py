from env.sol import env

import psycopg2
import pymongo
import time


def connect():
    ''' Connects to PostgreSLQL database and return cursor object
    '''

    conn = psycopg2.connect(
        dbname=env.pg_database,
        port=env.pg_port,
        user=env.pg_username,
        password=env.pg_password,
        host=env.pg_host
    )

    cur = conn.cursor()

    return(cur, conn)


def createTable(cur):
    ''' Creates table if it doesn't exist
        Runs one time on script start up
    '''

    cur.execute("CREATE TABLE IF NOT EXISTS \
        inspections \
        (gid serial, \
        name text, \
        complete boolean, \
        point geometry(Point, 4326));"
    )


def initMongo():
    ''' Initialize MongoDB connection
        Returns connection
    '''
    
    CLIENT = pymongo.MongoClient(f"mongodb://{env.mongodb_ip}:{env.mongodb_port}")
    DB = CLIENT[env.database]

    return(DB)


def getAssets(DB):
    ''' Gets list of assets
    '''

    assets = DB['ims_assets'].find(
        {
            '$or' : [
                {'type_id' : 1},
                {'type_id' : 4},
            ],
            '$and' : [
                {'is_deleted' : False}
            ]
        }
    )

    assets= list(assets)

    return(assets)


def getLocations(DB):
    ''' Gets latest loation of each asset
    '''

    locations = DB['ims_locations'].find()

    locations = list(locations)

    return(locations)


def parseLocations(assets, locations):
    ''' 
    '''

    processed = [] 

    for asset in assets:
        # I don't know, copied this form stack overflow
        # Looks up asset id in the locations and combines the two
        asset['location'] = next((item['location'] for item in locations if item["asset_id"] == asset['id']), None)

        # Skip if no location
        if asset['location'] == None:
            continue

        processed.append(asset)

    return(processed)


def insertDB(cur, locations):
    ''' Update (insert) data into PostgreSQL db
    '''

    for location in locations:
        # Update row with new data
        cur.execute(f"UPDATE inspections \
            SET (complete, point) =\
            ( False, ST_SetSRID(ST_MakePoint({location['location'][0]},{location['location'][1]}), 4326)) \
            WHERE name = '{location['name']}';")
        
        # Insert new row if nothing was updated
        if cur.rowcount == 0:
            cur.execute(f"INSERT INTO inspections \
                (name, complete, point) \
                VALUES \
                ('{location['name']}', True, ST_SetSRID(ST_MakePoint({location['location'][0]},{location['location'][1]}), 4326)) \
            ")          



def run():
    ''' Main run function
    '''
    # Establish PostgreSQL connection and create table if it doesn't exist
    # ONCE per script startup
    cur, conn = connect()
    createTable(cur)

    # Initialize Mongo connection
    DB = initMongo()

    while True:
        assets = getAssets(DB)
        locations = getLocations(DB)
        locations = parseLocations(assets, locations)

        # TODO: Get inspection status here

        insertDB(cur, locations)


        cur.close()
        conn.commit()

        time.sleep(60)


if __name__ == '__main__':

    run()