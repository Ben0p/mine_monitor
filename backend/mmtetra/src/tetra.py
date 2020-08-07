
from env.sol import env

import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
import datetime
import mysql.connector

from queries import nodes, subs, groups, calls


# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]

# Initialize MySQL connection
SQL = mysql.connector.connect(
  host=f"{env['tetra_sql_host']}",
  user=f"{env['tetra_sql_user']}",
  passwd=f"{env['tetra_sql_passwd']}",
  database=f"{env['tetra_sql_database']}",
  autocommit=True
)


def getMaintenance(CURSOR):
    # Execute MySQL query
    CURSOR.execute("SELECT * from databasemaintenancevalues;")
    myresult = CURSOR.fetchall()

    next_maint = myresult[0][2]
    next_maint = time.mktime(next_maint.timetuple())
    
    maint_start = next_maint - (30 * 60)
    maint_end = next_maint + (2 * 60 * 60)
    time_remaining = maint_end - time.time()
    time_remaining = round(time_remaining)

    if maint_start < time.time() < maint_end:
        under_maintenance = True
    else:
        under_maintenance = False
    
    return(under_maintenance, time_remaining)



def main():

    # Polling interval counter
    subscriber_count = 0
    group_count = 0

    # Do initial subscriber update
    # subs.tetraSubscribers(CURSOR, DB)

    while True:
        CURSOR = SQL.cursor()
        # Get DB maintenance time
        under_maintenance, time_remaining = getMaintenance(CURSOR)

        # Sleep for 60 and skip iteration if under maintenance
        if under_maintenance:
            print(f"DB under maintenance, sleeping for {time_remaining} sec...")
            CURSOR.close()
            time.sleep(time_remaining)
            continue


        nodes.tetraNodes(CURSOR, DB)
        time.sleep(0.5)
        calls.group(CURSOR, DB, seconds=60)
        time.sleep(0.5)
        calls.individual(CURSOR, DB, seconds=60)
        time.sleep(0.5)
        calls.sds(CURSOR, DB, seconds=60)

        group_count += 1
        subscriber_count += 1
        
        if group_count >= 6:
            group_count = 0
            time.sleep(0.5)
            groups.attachment(CURSOR, DB)
            time.sleep(0.5)
            subs.msLocation(CURSOR, DB)
            time.sleep(2)
            calls.groupDay(CURSOR, DB)
            time.sleep(2)
            calls.individualDay(CURSOR, DB)
            time.sleep(2)

        if subscriber_count >= 60:
            subscriber_count = 0
            time.sleep(2)
            subs.tetraSubscribers(CURSOR, DB)

        CURSOR.close()
        print("Closed cursor, sleeping for 10 sec")
        time.sleep(10)


if __name__ == "__main__":

    main()
