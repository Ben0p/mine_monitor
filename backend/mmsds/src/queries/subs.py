from env.sol import env

import time


def tetraSubscribers(CURSOR, DB):

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