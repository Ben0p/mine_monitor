from env.sol import env

import psycopg2
import pymongo
import time
from datetime import datetime, timedelta


def initPSQL():
    ''' Connects to PostgreSQL database and return cursor object
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

    cur.execute("CREATE TABLE IF NOT EXISTS inspections (gid serial, name text, color_hex text, opacity text, point geometry(Point, 4326));")


def initMongo():
    ''' Initialize MongoDB connection
        Returns connection
    '''

    CLIENT = pymongo.MongoClient(
        f"mongodb://{env.mongodb_ip}:{env.mongodb_port}")
    DB = CLIENT[env.database]

    return(DB)


def getAssets(DB):
    ''' Gets list of assets
    '''

    assets = DB['ims_assets'].find(
        {
            '$or': [
                {'type_id': 1},
                {'type_id': 4},
            ],
            '$and': [
                {'is_deleted': False}
            ]
        }
    )

    assets = list(assets)

    return(assets)


def getWeek():
    ''' Get the start of the work week (Sunday midnight)
    '''

    # Today
    start = datetime.now()
    start = start + timedelta(hours=env.time_offset)
    # Start of work week (Monday)
    start = start - timedelta(days=start.weekday())

    # Make it midnight
    start = start.replace().replace(hour=0, minute=0, second=0, microsecond=0)

    return(start)


def getAudits(DB, work_week):
    ''' Gets the pre-processed audits from MongoDB for the current work week
        Only gets specified audit temaple names
    '''

    audits = DB['ia_inspections'].find(
        {
            '$or': [
                {'template_data.metadata.name': "Tier 1 Tower Inspections"},
                {'template_data.metadata.name': "Trailer Inspection/Impedance check"},
                {'template_data.metadata.name': "Tier 2 Tower Inspection/Impedance check"},
            ],
            '$and': [
                {
                    'modified_at': {
                        '$gte': work_week
                    }
                }
            ]
        }
    )

    audits = list(audits)

    return(audits)


def getOrders(DB, work_week):
    ''' Gets the pre-processed SAP work orders for the current work week
    '''

    orders = DB['inspections'].find(
        {
            "$or": [
                {
                    'Earlstartdate': {
                        '$gte': work_week
                    }
                },
                {
                    'Basstartdate': {
                        '$gte': work_week
                    }
                }
            ]
        }
    )

    orders = list(orders)

    return(orders)


def matchOrders(ims_assets, work_orders):
    ''' Finds asset name matches in the work orders
    '''

    matched_assets = []

    for asset in ims_assets:

        asset_name = asset['name'].replace('-', '')

        for work_order in work_orders:
            if asset_name in work_order['FunctionalLoc']:
                matched_assets.append(asset)
            elif asset['note']:
                if work_order['FunctionalLoc'] in asset['note']:
                    matched_assets.append(asset)

    return(matched_assets)


def matchAudits(assets, audits):
    ''' Matches assets with audits
    '''

    matched_audits = []

    for asset in assets:
        for audit in audits:
            try:
                if asset['name'] in audit['audit_data']['site']['name']:
                    matched_audits.append(asset)
                site = True
            except KeyError:
                site = False

            if not site:
                if asset['name'] in audit['audit_data']['name']:
                    matched_audits.append(asset)

    return(matched_audits)


def processResults(matched_assets, ims_assets, matched_audits):
    ''' Prepares results for insertion into PostGreSQL
    '''

    final_results = []

    # Not due for inspection
    for ims_asset in ims_assets:

        if ims_asset['location']:
            asset = {}
            asset['display'] = False
            asset['name'] = ims_asset['name']
            asset['color_hex'] = '#ff3d71'
            asset['lon'] = str(ims_asset['location']['location'][0])
            asset['lat'] = str(ims_asset['location']['location'][1])


        final_results.append(asset)

    # Due for inspeciton
    for matched_asset in matched_assets:

        if matched_asset['location']:
            asset = {}
            asset['display'] = True
            asset['name'] = matched_asset['name']
            asset['color_hex'] = '#ff3d71'
            asset['lon'] = str(matched_asset['location']['location'][0])
            asset['lat'] = str(matched_asset['location']['location'][1])
            final_results.append(asset)


    # Complete
    for matched_audit in matched_audits:

        for i in range(len(final_results)):
            if final_results[i]['name'] == matched_audit['name']:
                del final_results[i]
                break

        asset = {}
        asset['display'] = True
        asset['name'] = matched_audit['name']
        asset['color_hex'] = '#00d68f'
        asset['lon'] = str(matched_audit['location']['location'][0])
        asset['lat'] = str(matched_audit['location']['location'][1])
        final_results.append(asset)

    return(final_results)


def insertDB(cur, results):
    ''' Update (insert) data into PostgreSQL db
    '''

    for result in results:
        # Update row with new data
        cur.execute(f"UPDATE inspections SET (display, color_hex, point) =\
            ({result['display']}, \
            '{result['color_hex']}',\
            ST_SetSRID(ST_MakePoint({result['lon']},\
            {result['lat']}), 4326))\
            WHERE name = '{result['name']}';")

        # Insert new row if nothing was updated
        if cur.rowcount == 0:
            cur.execute(f"INSERT INTO inspections \
                (name, display, color_hex, point) \
                VALUES \
                ('{result['name']}', {result['display']}, '{result['color_hex']}', ST_SetSRID(ST_MakePoint({result['lon']},{result['lat']}), 4326)) \
            ")


def run():
    ''' Main run function
    '''
    # Establish PostgreSQL connection and create table if it doesn't exist
    # ONCE per script startup
    cur, conn = initPSQL()
    conn.autocommit = True

    # Create table disabled because not really required (left it in for reference)
    # createTable(cur)

    # Initialize Mongo connection
    DB = initMongo()

    while True:

        start_time = time.time()
        # Get IMS assets with locations
        ims_assets = getAssets(DB)
        print(f"Retrieved {len(ims_assets)} IMS assets")

        # Get current week
        work_week = getWeek()
        print(f"Current week start: {work_week}")

        # Get iAuditor audites for current work week
        audits = getAudits(DB, work_week)
        print(f"Retrieved {len(audits)} audits")

        # Get SAP work orders for current work week
        work_orders = getOrders(DB, work_week)
        print(f"Retrieved {len(work_orders)} work orders")

        # Match and filter work orders with assets
        matched_assets = matchOrders(ims_assets, work_orders)
        print(f"Matched {len(matched_assets)} work orders")

        # Match audits with filtered assets
        matched_audits = matchAudits(matched_assets, audits)
        print(f"Matched {len(matched_audits)} audits")

        # Colorize
        final_results = processResults(
            matched_assets, ims_assets, matched_audits)
        print(f"Processed {len(final_results)} assets")

        insertDB(cur, final_results)
        print(f"Updated layer")

        conn.commit()

        finish_time = time.time()
        total_time = finish_time - start_time
        total_time = round(total_time, 2)

        print(f"Completed in {total_time} seconds")

        print("Sleep 60sec")
        time.sleep(60)


if __name__ == '__main__':

    run()
