from env.sol import env

import time
import datetime



def group(CURSOR, DB, seconds=60):
    '''Get Tetra unique group call count last 60 seconds
    '''

    # MySQL query
    CURSOR.execute(f"SELECT \
        COUNT(DISTINCT CallId) \
        from groupcall \
        WHERE \
        CallInitEsn \
        NOT LIKE '' \
        AND CallBegin > date_sub(now(), \
        interval {28800 + seconds} second);")
    myresult = CURSOR.fetchall()

    # First column of first row (count result)
    gr_calls_per_sec = round(int(myresult[0][0] or 0) / seconds, 2)

    DB['tetra_call_stats'].find_one_and_update(
        {
            'range_sec' : seconds,
            'type' : 'group'
        },
        {
            '$set': {
                'calls' : myresult[0][0],
                'calls_sec': gr_calls_per_sec
            }
        },
        upsert=True
    )

    print(f"{time.strftime('%d/%m/%Y %X')} - Retreived group calls last {seconds}sec")


def individual(CURSOR, DB, seconds=60):
    ''' Get Tetra unique individual call count last 60 seconds
    '''

    # MySQL Query
    CURSOR.execute(f"SELECT \
        COUNT(DISTINCT CallId) \
        from individualcall \
        WHERE CallInitiated > date_sub(now(), \
        interval {28800 + seconds} second);")
    myresult = CURSOR.fetchall()

    # First column of first row (count result)
    in_calls_per_sec = round(int(myresult[0][0] or 0) / seconds, 2)

    # Insert into Mongo
    DB['tetra_call_stats'].find_one_and_update(
        {
            'range_sec' : seconds,
            'type' : 'individual'
        },
        {
            '$set': {
                'calls' : myresult[0][0],
                'calls_sec': in_calls_per_sec
            }
        },
        upsert=True
    )
    print(f"{time.strftime('%d/%m/%Y %X')} - Retreived individual calls last {seconds}sec")


def sds(CURSOR, DB, seconds=60):

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


def groupDay(CURSOR, DB):
    ''' Gets group calls for the past 24 hours and gets totals per minute
    This is some serious wizard jizz
    '''
    #115200 seconds = 24 hours +8 Timezone
    interval = (24*60*60) + (8*60*60)
    # MySQL query
    CURSOR.execute(f"SELECT \
        DISTINCT \
        CallId, \
        CallBegin\
        FROM \
        groupcall \
        WHERE \
        CallInitEsn \
        NOT LIKE '' \
        AND CallBegin > date_sub(now(), \
        interval {interval} second);")
    myresult = CURSOR.fetchall()

    # Reset minute dictionary and call arrays
    minutes = {}
    call_counts = []
    call_minutes = []

    # Unix time - (24 hours in seconds)
    one_day_ago = time.time() - 86400

    # Generate a dictionary of minutes for the past 24 hours (the minute is the key)
    # In 60 second steps up to 86400 (24 hours)
    for step in range(0, 86400, 60):
        # Get the second from 24 hours ago (+ step)
        minute = one_day_ago + step
        # Format it into a datestamp rounded to the minute
        minute = datetime.datetime.fromtimestamp(minute+28800).strftime('%d/%m/%Y %H:%M')
        minutes[minute] = 0

    # For each call (row) in the MySQL query...
    for call in myresult:
        # Get the timestamp (+8 hours)
        minute = call[1].timestamp()+28800
        # Format into the minute rounded timestamp
        minute = datetime.datetime.fromtimestamp(minute).strftime('%d/%m/%Y %H:%M')
        try:
            minutes[minute] += 1
        except KeyError:
            pass

    # Separate the key:values into separate arrays (for graph front end)
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


def individualDay(CURSOR, DB):
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
