
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
    radios = 0

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
        AND Description NOT LIKE 'ELI%' \
        AND Description NOT LIKE 'New%';"
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

        ts_idle += int(x[4] or 0)
        ts_in += int(x[6] or 0)
        ts_gr += int(x[7] or 0)
        ts_mc += int(x[8] or 0)
        ts_sc += int(x[9] or 0)
        radios += int(x[3] or 0)

        online = True

        # Override if offline   
        if x[0].timestamp() < (time.time()-28810):
            color = 'offline'
            online = False
            load = 100

        
        
        node_names.append(x[2])
        node_loads.append(round(load))
        node_colors.append(color)


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
                    'color' : color,
                    'online' : online
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

    DB['tetra_radio_count'].find_one_and_update(
        {
            'node' : 'all',
        },
        {
            '$set': {
                'node' : 'all',
                'name' : 'Total',
                'status' : 'success',
                'online' : True,
                'count' : radios,
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
                ],
                'ts_load' : [
                    ts_idle,
                    ts_in,
                    ts_gr,
                ],
                'ts_colors' : [
                    'success',
                    'danger',
                    'warning',
                ]
            }
        },
        upsert=True
    )

    print(f"{time.strftime('%d/%m/%Y %X')} - Updated node status")




def genPoints(points, start, finish):
    print(start)
    print(type(start))

    return(None)



def tetraNodesMinute():
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
        NodeNo, \
        Description, \
        StatusCount, \
        TimeFirst, \
        TimeLast, \
        TrafficTsPeak, \
        ItchAvg, \
        GtchAvg, \
        IdleAvg, \
        MissingTsAvg, \
        TotalTsAvg, \
        RadioCellCongestionTchPct, \
        RadioCellCongestionFreePct, \
        RadioCellCongestionMissingPct \
        FROM `nodestatisticsrestenminute` \
        WHERE Description NOT LIKE 'ELI%' \
        AND Description NOT LIKE 'New%';"
    )

    myresult = CURSOR.fetchall()

    #points = genPoints(myresult[0][3], myresult[0][4], myresult[0][5])

def tetraSubscribers():

    # Execute MySQL query
    CURSOR.execute("SELECT \
        SSI, \
        Description, \
        SsiKind \
        FROM `subscriber`;"
    )

    myresult = CURSOR.fetchall()

    for subscriber in myresult:

        if subscriber[2] == 1:
            s_type = 'Subscriber'
        elif subscriber[2] == 2:
            s_type = 'Group'
        elif subscriber[2] == 5:
            s_type = 'Application'
        elif subscriber[2] == 8:
            s_type = 'Terminal'

        
        DB['tetra_subscribers'].find_one_and_update(
            {
                'ssi' : subscriber[0],
            },
            {
                '$set': {
                    'ssi' : subscriber[0],
                    'description' : subscriber[1],
                    'type' : s_type,
                    'group' : 'None'
                }
            },
            upsert=True
        )
    print(f"{time.strftime('%d/%m/%Y %X')} - Refreshed subscribers")

def groupAttachment():

    # Execute MySQL query
    CURSOR.execute("SELECT \
        Ssi, \
        GroupSsi, \
        Selected \
        FROM `groupattachment` \
        WHERE Selected = 1;"
    )

    myresult = CURSOR.fetchall()

    groups_list = DB['tetra_subscribers'].find(
        {
            'type' : 'Group'
        }
    )

    groups = {group['ssi'] : group['description'] for group in groups_list}


    for subscriber in myresult:

        attached_group = subscriber[1]
        talkgroup = groups[attached_group]
        
        
        DB['tetra_subscribers'].find_one_and_update(
            {
                'ssi' : subscriber[0],
            },
            {
                '$set': {
                    'talkgroup' : talkgroup
                }
            },
            upsert=True
        )
    print(f"{time.strftime('%d/%m/%Y %X')} - Retrieved current group attachment")

def groupCalls(seconds):
    CURSOR.execute(f"SELECT \
        DISTINCT \
        CallId, \
        CallInitEsn, \
        CallSetupTimeMs, \
        OriginatingNodeNo, \
        CallingEsn, \
        InitRssi, \
        InitMsDistance \
        FROM \
        groupcall \
        WHERE \
        CallInitEsn \
        NOT LIKE '' \
        AND CallBegin > date_sub(now(), \
        interval {28800 + seconds} second);")
    
    myresult = CURSOR.fetchall()

    call_count = len(myresult)
    
    gr_calls_per_sec = round(int(call_count or 0) / seconds, 2)

    DB['tetra_call_stats'].find_one_and_update(
        {
            'range_sec' : seconds,
            'type' : 'group'
        },
        {
            '$set': {
                'calls' : call_count,
                'calls_sec': gr_calls_per_sec
            }
        },
        upsert=True
    )
    print(f"{time.strftime('%d/%m/%Y %X')} - Retreived group calls last {seconds}sec")


def individualCalls(seconds):
    CURSOR.execute(f"SELECT \
        DISTINCT \
        CallId, \
        CallInitEsn, \
        CallSetupTimeMs, \
        OriginatingNodeNo, \
        CallingEsn, \
        CallInitRssi, \
        CallInitMsDistance \
        FROM \
        individualcall \
        WHERE \
        CallInitiated > date_sub(now(), \
        interval {28800 + seconds} second);")
    
    myresult = CURSOR.fetchall()

    call_count = len(myresult)
    
    in_calls_per_sec = round(int(call_count or 0) / seconds, 2)

    DB['tetra_call_stats'].find_one_and_update(
        {
            'range_sec' : seconds,
            'type' : 'individual'
        },
        {
            '$set': {
                'calls' : call_count,
                'calls_sec': in_calls_per_sec
            }
        },
        upsert=True
    )
    print(f"{time.strftime('%d/%m/%Y %X')} - Retreived individual calls last {seconds}sec")


def groupCallsDay():
    #115200 seconds = 24 hours +8 Timezone
    CURSOR.execute(f"SELECT \
        DISTINCT \
        CallId, \
        CallBegin,\
        CallInitEsn, \
        CallSetupTimeMs, \
        OriginatingNodeNo, \
        CallingEsn, \
        InitRssi, \
        InitMsDistance \
        FROM \
        groupcall \
        WHERE \
        CallInitEsn \
        NOT LIKE '' \
        AND CallBegin > date_sub(now(), \
        interval 115200 second);")
    
    myresult = CURSOR.fetchall()

    minutes = {}
    call_counts = []
    call_minutes = []

    one_day_ago = time.time() - 115200

    for step in range(0, 86400, 60):
        minute = one_day_ago + step
        minute = datetime.datetime.fromtimestamp(minute+28800).strftime('%d/%m/%Y %H:%M')
        minutes[minute] = 0

    for call in myresult:
        minute = call[1].timestamp()+28800
        minute = datetime.datetime.fromtimestamp(minute).strftime('%d/%m/%Y %H:%M')
        try:
            minutes[minute] += 1
        except KeyError:
            pass

    
    for key, value in minutes.items():
        call_minutes.append(key)
        call_counts.append(value) 

    DB['tetra_call_stats'].find_one_and_update(
        {
            'range' : 'day',
            'type' : 'history'
        },
        {
            '$set': {
                'minutes' : call_minutes,
                'group_calls' : call_counts,
            }
        },
        upsert=True
    )
    print(f"{time.strftime('%d/%m/%Y %X')} - Retreived group call counts last day")

def IndividualCallsDay():
    #115200 seconds = 24 hours +8 Timezone
    CURSOR.execute(f"SELECT \
        DISTINCT \
        CallId, \
        CallInitiated,\
        CallInitEsn, \
        CallSetupTimeMs, \
        OriginatingNodeNo, \
        CallingEsn, \
        CallInitRssi, \
        CallInitMsDistance \
        FROM \
        individualcall \
        WHERE \
        CallInitiated > date_sub(now(), \
        interval 115200 second);")
    
    myresult = CURSOR.fetchall()

    minutes = {}
    call_counts = []
    call_minutes = []

    one_day_ago = time.time() - 115200

    for step in range(0, 86400, 60):
        minute = one_day_ago + step
        minute = datetime.datetime.fromtimestamp(minute+28800).strftime('%d/%m/%Y %H:%M')
        minutes[minute] = 0

    for call in myresult:
        try: 
            minute = call[1].timestamp()+28800
            minute = datetime.datetime.fromtimestamp(minute).strftime('%d/%m/%Y %H:%M')
        except AttributeError:
            pass
        try:
            minutes[minute] += 1
        except KeyError:
            pass

    
    for key, value in minutes.items():
        call_minutes.append(key)
        call_counts.append(value) 

    DB['tetra_call_stats'].find_one_and_update(
        {
            'range' : 'day',
            'type' : 'history'
        },
        {
            '$set': {
                'minutes' : call_minutes,
                'individual_calls' : call_counts,
            }
        },
        upsert=True
    )
    print(f"{time.strftime('%d/%m/%Y %X')} - Retreived individual call counts last day")

def main():

    subscriber_count = 0
    group_count = 0


    while True:

        tetraNodes()
        time.sleep(2)
        groupCalls(10)
        time.sleep(2)
        individualCalls(10)

        group_count += 1
        subscriber_count += 0
        
        if group_count >= 6:
            group_count = 0
            time.sleep(2)
            groupAttachment()
            time.sleep(2)
            groupCallsDay()
            time.sleep(2)
            IndividualCallsDay()
            time.sleep(2)

        if subscriber_count >= 60:
            subscriber_count = 0
            time.sleep(2)
            tetraSubscribers()

        #tetraNodesMinute()

        time.sleep(10)

if __name__ == "__main__":

    main()
