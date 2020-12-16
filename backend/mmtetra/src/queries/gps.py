from env.sol import env

import time
import datetime



def faultyGPS(CURSOR, DB):
    ''' Selects unique sdsdata rows with data length of 44 
        Data length 44 -> no GPS data
    '''

    # One week
    interval = 604800

    # Execute MySQL query NO GPS
    CURSOR.execute(f"SELECT DISTINCT \
        s.CallingSsi, \
        s.CallingDescr \
	    FROM sdsdata s \
        WHERE s.UserDataLength = 44 \
        and s.Timestamp > date_sub(now(), \
        interval {interval} second);"
    )

    no_gps_results = CURSOR.fetchall()
    no_gps = [x[0] for x in no_gps_results]
    busted_dict = {x[0] : x[1] for x in no_gps_results}

    # Execute MySQL query WORKING GPS
    CURSOR.execute(f"SELECT DISTINCT \
        s.CallingSsi \
	    FROM sdsdata s \
        WHERE s.UserDataLength = 129 \
        and s.Timestamp > date_sub(now(), \
        interval {interval} second);"
    )

    working_gps = CURSOR.fetchall()
    working_gps = [x[0] for x in working_gps]

    busted = list(set(no_gps) - set(working_gps))

    subscriber_list = DB['tetra_subscribers'].find()

    subs = {}

    for sub in subscriber_list:

        try:
            description = sub['description']
        except:
            description = ''

        try:
            comment = sub['comment']
        except:
            comment = ''


        subs[sub['ssi']] = {
            'description' : description,
            'comment' : comment
        }


    with open("busted_gps.csv", 'w') as f:
        f.write("ISSI,Calling Description,Subscriber List,Comment\n")
        for issi in busted:
            f.write(f"{issi}, {busted_dict[issi]}, {subs[issi]['description']}, {subs[issi]['comment']} \n")
        f.close()


