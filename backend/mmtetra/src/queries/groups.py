from env.sol import env

import time




def attachment(CURSOR, DB):

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

        try:
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
        except KeyError:
            pass


    print(f"{time.strftime('%d/%m/%Y %X')} - Retrieved current group attachment")