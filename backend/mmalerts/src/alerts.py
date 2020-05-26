#! /usr/bin/python3.7

from env.sol import env

from xml.etree import ElementTree
import requests
import pymongo
from bson.json_util import dumps
import json
import copy
import time
import json
from pyModbusTCP.client import ModbusClient
import subprocess
import platform
import os
import hashlib


""""Alert polling script
Production and development environment variabes in env
Retrieves data from mongo db
Polls coil status of modbus devices
Writes results back in mongo
"""

# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(
    f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]


def checkDB():
    alert_types = ['Sign', 'Beacon', 'Trailer']
    dbs = CLIENT.list_databases()

    if env['database'] not in dbs:
        for alert in alert_types:
            DB['alert_types'].insert_one(
                {
                    "name": alert
                }
            )
        print("Created new DB")
    else:
        print("Found Databse")


def getModules():
    '''Returns array of alert modules'''

    modules = DB['alert_modules'].find()

    return(list(modules))


def getAlerts():
    '''Returns array of alert modules'''

    alerts = DB['alert_all'].find()

    return(list(alerts))


def ping(host):
    """Returns True and latency if host responds to a ping request
    host = ipv4 address
    """

    if platform.system().lower() == "windows":

        try:
            response = subprocess.check_output(
                ['ping', '-n', '1', host],
                stderr=subprocess.STDOUT,  # get all output
                universal_newlines=True,  # return string not bytes
                shell=False
            )
            latencies = response.splitlines()[7]
            latency = latencies.split('=')[3][1]
            result = True
        except subprocess.CalledProcessError:
            latency = 999
            result = False
        except IndexError:
            latency = 999
            result = False
    else:
        try:
            response = subprocess.check_output(
                ['ping', '-c', '1', host]
            )
            latencies = response.splitlines()[5]
            latency = latencies.decode().split('/')[4][0]
            result = True
        except subprocess.CalledProcessError:
            latency = 999
            result = False

    return(result, latency)


def restAPI(ip):
    """Checks for active Rest API on supplied ip"""

    # xml url
    do_xml = 'http://{}/digitaloutput/all/value'.format(ip)
    # Use requests to authenticate http session and get xml
    with requests.Session() as session:
        try:
            response = session.get(do_xml, auth=(
                env['module_user'], env['module_pass']), timeout=1)
            # Placeholder for xml response data (potential future use)
            ElementTree.fromstring(response.content)
            return(True)
        except:
            return(False)


def modbus(ip):
    """Get output states via modbus over ip"""

    # Setup modbus connection
    c = ModbusClient(host=ip, port=502, auto_open=True)
    # Read Modbus outputs
    bits = c.read_coils(16, 6)
    # If there is a response
    if bits:
        # Set output states
        return([bits[0], bits[1], bits[2], bits[3], bits[4], bits[5]])
    else:
        return(['', '', '', '', '', ''])


def cleanUp(module):
    alerts = getAlerts()

    for alert in alerts:
        count = DB['alert_modules'].count_documents(
            {
                'name': alert['name']
            }
        )

        if count < 1:
            DB['alert_all'].delete_many(
                {'name': alert['name']}
            )
            print("Deleted {}".format(alert['name']))


def writeDB(alert):

    print("Updating "+alert['name'])
    DB['alert_all'].find_one_and_update(
        {
            'name': alert['name']
        },
        {
            '$set': {
                'name': alert['name'],
                'location': alert['location'],
                'zone': alert['zone'],
                'ip': alert['ip'],
                'online': alert['online'],
                'rest': alert['rest'],
                'type': alert['type'],
                'status': alert['status'],
                'icon': alert['icon'],
                'state': alert['state'],
                'latency': alert['latency'],
                'all_clear': alert['all_clear'],
                'emergency': alert['emergency'],
                'lightning': alert['lightning'],
                'a':  alert['a'],
                'b':  alert['b'],
                'c': alert['c']
            }
        },
        upsert=True
    )


def getAll():
    """Main function"""

    modules = getModules()
    cleanUp(modules)

    # For each module
    for module in modules:
        # module['name'] = module['name']
        # module['type'] = module['type']
        # module['zone'] = module['zone']
        # module['location'] = module['location']
        # module['ip] = module['ip']

        # Remove the mongo id
        module.pop('_id', None)
        if module['ip']:
            online, latency = ping(module['ip'])
        else:
            online = False
        module['online'] = online
        module['latency'] = latency

        if not online:
            module['status'] = 'primary'
            module['icon'] = 'close-circle-outline'
            module['state'] = 'Offline'
            module['rest'] = False
            module['all_clear'] = False
            module['emergency'] = False
            module['lightning'] = False
            module['a'] = False
            module['b'] = False
            module['c'] = False
        else:
            outputs = modbus(module['ip'])
            module['rest'] = restAPI(module['ip'])
            if outputs[0]:
                module['state'] = 'All Clear'
                module['status'] = 'success'
                module['icon'] = 'checkmark-circle-2-outline'
            elif outputs[1]:
                module['state'] = 'Emergency'
                module['status'] = 'danger'
                module['icon'] = 'alert-circle-outline'
            elif outputs[3]:
                module['state'] = 'A Alert'
                module['status'] = 'info'
                module['icon'] = 'flash-outline'
            elif outputs[4]:
                module['state'] = 'B Alert'
                module['status'] = 'warning'
                module['icon'] = 'flash-outline'
            elif outputs[5]:
                module['state'] = 'C Alert'
                module['status'] = 'danger'
                module['icon'] = 'flash-outline'
            else:
                module['status'] = 'primary'
                module['icon'] = 'close-circle-outline'
                module['state'] = 'Offline'
                module['rest'] = False

            module['all_clear'] = outputs[0]
            module['emergency'] = outputs[1]
            module['lightning'] = outputs[2]
            module['a'] = outputs[3]
            module['b'] = outputs[4]
            module['c'] = outputs[5]

        writeDB(module)


def genWZKey():
    day = time.strftime('%d')
    month = time.strftime('%m')
    year = time.strftime('%y')

    key = (int(day) * 2) + (int(month) * 300) + (int(year) * 170000)
    key = f"{key}{env['weatherzone_password']}"
    key = hashlib.md5(key.encode('utf-8')).hexdigest()

    return(key)


def weatherZone():

    key = genWZKey()

    url = f'http://ws1.theweather.com.au/?lt=uwas&lc=183,179,180,574,570,1443,1442&alerts=1(client=337)&format=json&u=15566-1804&k={key}'
    print(url)

    response = requests.get(url=url, proxies={"http":env['proxy']})
    json_data = json.loads(response.text)

    locations = json_data['countries'][0]['locations']
    
    for location in locations:
        for alert in location['alerts']:
            if alert['embargo_period'] != 'Infinite' and alert['alert_type'] == 'LIGHTNING':
                print(f"{location['name']} - {alert['status']}")
                if alert['status'] == "CLEAR":
                    state = 'All Clear'
                    status = "success"
                    icon = "checkmark-circle-2-outline"
                elif alert['status'] == "Alpha":
                    state = 'A Alert'
                    status = 'info'
                    icon = 'flash-outline'
                elif alert['status'] == "Bravo":
                    state = 'B Alert'
                    status = 'warning'
                    icon = 'flash-outline'
                elif alert['status'] == "Charlie":
                    state = 'C Alert'
                    status = 'danger'
                    icon = 'flash-outline'
                else:
                    status = 'primary'
                    state = 'Offline'
                    icon = 'close-circle-outline'
            elif alert['embargo_period'] == 'Infinite' and alert['alert_type'] == 'LIGHTNING':
                print(f"{location['name']} - {alert['status']}")
                if alert['status'] == "CLEAR":
                    state = 'All Clear'
                    status = "success"
                    icon = "checkmark-circle-2-outline"

        DB['alert_wz'].find_one_and_update(
            {
                'name': location['name']
            },
            {
                '$set': {
                    'online' : True,
                    'name' : location['name'],
                    'zone' : location['name'],
                    'status' : status,
                    'state' : state,
                    'icon' : icon
                }
            },
            upsert=True
        )
    
    print("Polled Weather Zone")

if __name__ == '__main__':

    checkDB()

    while True:
        getAll()
        weatherZone()
        time.sleep(10)
