
from env.sol import env

import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
import datetime
import mysql.connector


# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]

# Initialize mySQL connection
SQL = mysql.connector.connect(
  host=f"{env['tetra_sql_host']}",
  user=f"{env['tetra_sql_user']}",
  passwd=f"{env['tetra_sql_passwd']}",
  database=f"{env['tetra_sql_database']}"
)

CURSOR = SQL.cursor()


def tetraNodes():

    node_names = []
    node_loads = []
    node_colors = []
    
    ts_idle = 0
    ts_in = 0
    ts_gr = 0
    ts_mc = 0
    ts_sc = 0

    # Execute MySQL query
    CURSOR.execute("SELECT \
        Timestamp, \
        NodeNo, \
        Description, \
        RadioRegMsCount, \
        RadioTsCountIdle, \
        RadioTsCountTotal, \
        RadioTsCountItch, \
        RadioTsCountGtch, \
        RadioTsCountMcch, \
        RadioTsCountScch \
        FROM `nodestatus` \
        WHERE StdBy = '0' \
        AND Description NOT LIKE 'ELI%';"
    )

    myresult = CURSOR.fetchall()


    for x in myresult:

        ts_used = int(x[5] or 0) - int(x[4] or 0)

        try:
            load = ts_used / int(x[5] or 0) * 100
        except ZeroDivisionError:
            load = 0

        if load >= 90:
            color = 'danger'
        elif 90 > load >= 75:
            color = 'warning'
        elif 75 > load >= 0:
            color = 'success'


        node_names.append(x[2])
        node_loads.append(round(load))
        node_colors.append(color)

        ts_idle += int(x[4] or 0)
        ts_in += int(x[6] or 0)
        ts_gr += int(x[7] or 0)
        ts_mc += int(x[8] or 0)
        ts_sc += int(x[9] or 0)


        DB['tetra_nodes'].find_one_and_update(
            {
                'node_number': x[1],
            },
            {
                '$set': {
                    'timestamp' : x[0],
                    'node_number' : x[1],
                    'node_description' : x[2],
                    'radio_count' : x[3],
                    'ts_idle' : x[4],
                    'ts_total' : x[5],
                    'ts_in' : x[6],
                    'ts_gr' : x[7],
                    'ts_mc' : x[8],
                    'ts_sc' : x[9],
                    'ts_used' : ts_used,
                    'load' : round(load),
                    'color' : color
                }
            },
            upsert=True
        )
    

    DB['tetra_node_load'].find_one_and_update(
        {
            'type': 'bar',
        },
        {
            '$set': {
                'node_names' : node_names,
                'node_loads' : node_loads,
                'node_colors' : node_colors
            }
        },
        upsert=True
    )




    DB['tetra_node_load'].find_one_and_update(
        {
            'type': 'radar',
        },
        {
            '$set': {
                'ts_type' : [
                    "Idle",
                    "Individual",
                    "Group",
                    "Main CC",
                    "Secondary CC"
                ],
                'ts_load' : [
                    ts_idle,
                    ts_in,
                    ts_gr,
                    ts_mc,
                    ts_sc
                ],
                'ts_colors' : [
                    'primary',
                    'danger',
                    'warning',
                    'success',
                    'info'
                ]
            }
        },
        upsert=True
    )



def main():
    tetraNodes()


if __name__ == "__main__":
    while True:

        main()

        time.sleep(10)