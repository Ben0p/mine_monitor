
from env.sol import env

import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
import datetime
import mysql.connector

from queries import nodes, subs


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

def msLocation():

    # Execute MySQL query
    CURSOR.execute("SELECT \
        Ssi, \
        NodeDescr \
        FROM `mslocation`"
    )

    myresult = CURSOR.fetchall()


    for subscriber in myresult:

        node = subscriber[1]        
        
        DB['tetra_subscribers'].find_one_and_update(
            {
                'ssi' : subscriber[0],
            },
            {
                '$set': {
                    'node' : node
                }
            },
            upsert=True
        )
    print(f"{time.strftime('%d/%m/%Y %X')} - Retrieved current node attachment")


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

def SdsCalls(seconds):
    CURSOR.execute(f"SELECT \
        COUNT(*) \
        FROM \
        sdsdata \
        WHERE \
        Timestamp >= date_sub(now(), \
        interval {28800 + seconds} second);")
    
    myresult = CURSOR.fetchall()
    
    in_calls_per_sec = round(int(myresult[0][0] or 0) / seconds, 2)

    DB['tetra_call_stats'].find_one_and_update(
        {
            'range_sec' : seconds,
            'type' : 'sds'
        },
        {
            '$set': {
                'calls' : myresult[0][0],
                'calls_sec': in_calls_per_sec
            }
        },
        upsert=True
    )
    print(f"{time.strftime('%d/%m/%Y %X')} - Retreived sds calls last {seconds}sec")

def groupCallsDay():
    #115200 seconds = 24 hours +8 Timezone
    interval = (24*60*60) + (8*60*60)
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
        interval {interval} second);")
    
    myresult = CURSOR.fetchall()

    minutes = {}
    call_counts = []
    call_minutes = []

    one_day_ago = time.time() - 86400

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

    one_day_ago = time.time() - 86400

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

    subs.tetraSubscribers(CURSOR, DB)

    while True:

        nodes.tetraNodes(CURSOR, DB)
        time.sleep(2)
        groupCalls(60)
        time.sleep(2)
        individualCalls(60)
        time.sleep(2)
        SdsCalls(60)

        group_count += 1
        subscriber_count += 1
        
        if group_count >= 6:
            group_count = 0
            time.sleep(2)
            groupAttachment()
            time.sleep(2)
            msLocation()
            time.sleep(2)
            groupCallsDay()
            time.sleep(2)
            IndividualCallsDay()
            time.sleep(2)

        if subscriber_count >= 60:
            subscriber_count = 0
            time.sleep(2)
            subs.tetraSubscribers(CURSOR, DB)

        #tetraNodesMinute()

        time.sleep(10)

if __name__ == "__main__":

    main()
