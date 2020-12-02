import time
from env.sol import env

def tetraNodes(CURSOR, DB):

    node_names = []
    node_loads = []
    node_colors = []
    node_subs = []
    node_subs_colors = []
    
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
        AND Description NOT LIKE 'New%' \
        AND Description NOT LIKE 'SOL_GW_NODE%' \
        AND Description NOT LIKE 'Solomon Server';"
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
        if x[0].timestamp() < (time.time()+ env['time_offset'] -15):
            color = 'offline'
            online = False
            load = 100
            radios += 0
            ts_idle = 0
            ts_in = 0
            ts_gr = 0
            ts_mc = 0
            ts_sc = 0
        
        node_names.append(x[2])
        node_loads.append(round(load))
        node_colors.append(color)
        node_subs.append(x[3])
        node_subs_colors.append('success')

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

    DB['tetra_node_subscribers'].find_one_and_update(
        {
            'type': 'bar',
        },
        {
            '$set': {
                'node_names' : node_names,
                'node_loads' : node_subs,
                'node_colors' : node_subs_colors
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