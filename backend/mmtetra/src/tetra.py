
from env.sol import env

import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
import datetime
import mysql.connector

from queries import nodes, subs, groups, calls, gps


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




def main():

    # Polling interval counter
    subscriber_count = 0
    group_count = 0

    # Do initial subscriber update
    # subs.tetraSubscribers(CURSOR, DB)

    while True:
        CURSOR = SQL.cursor()

        '''
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
        '''

        gps.faultyGPS(CURSOR, DB)
        CURSOR.close()
        print("Closed cursor, sleeping for 10 sec")
        time.sleep(10)


if __name__ == "__main__":

    main()
