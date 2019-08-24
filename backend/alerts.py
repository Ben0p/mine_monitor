#! /usr/bin/python3.7

from env.devprod import env
# from env.dev import env
# from env.prod import env
from xml.etree import ElementTree
import requests
import pymongo
from bson.json_util import dumps
import json
import copy
import time
import json
from pyModbusTCP.client import ModbusClient
import subprocess, platform
import os


""""Alert polling script
Production and development environment variabes in env
Retrieves data from mongo db
Polls coil status of modbus devices
Writes results back in mongo
"""

# Initialize mongo connection one time
CLIENT = pymongo.MongoClient('mongodb://{}:{}/'.format(env['mongodb_ip'], env['mongodb_port']))
DB = CLIENT[env['database']]


def getModules():
    '''Returns array of alert modules'''

    modules = DB['alert_modules'].find()

    return(list(modules))

def getLocations():
    '''Returns array of alert locations'''

    locations = DB['alert_locations'].find()
    location_names = [location for location in locations]

    return(location_names)

def getTypes():
    '''Returns array of alert types'''

    types = DB['alert_types'].find()
    types_names = [_type for _type in types]

    return(types_names)


def ping(host):
    """Returns True and latency if host responds to a ping request
    host = ipv4 address
    """

    if platform.system().lower()=="windows":

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
    do_xml = 'http://{ip}/digitaloutput/all/value'
    # Use requests to authenticate http session and get xml
    with requests.Session() as session:
        try:
            response = session.get(do_xml, auth=(env.module_user, env.module_pass), timeout=1)
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

def getStatus(modules):
    updated_list = []

    for module in modules:
        outputs = modbus(module['ip'])
        online, latency = ping(module['ip'])

        module['All Clear'] = outputs[0]
        module['Emergency'] = outputs[1]
        module['Lightning'] = outputs[2]
        module['A'] = outputs[3]
        module['B'] = outputs[4]
        module['C'] = outputs[5]
        module['online'] = online
        module['latency'] = latency


        updated_list.append(module)
    
    return(updated_list)


def writeDB(alert):
    print("Updating "+alert['location'])

    DB['alert_status'].find_one_and_update(
        {
            'location':alert['location']
        },
        {
            '$set': {
                'modules': alert['modules']
            }
        },
        upsert=True
    )

def getAll():
    """Main function"""

    # Generate array of alerts with location and IP
    locations = getModules()

    location = {}
    module_locations = []

    # For each module
    for modules in locations:
        modules_list = []
        for module in modules:
            online, latency = ping(module['ip'])
            module['online'] = online
            if not online:
                module['status'] = 'primary'
            else:
                outputs = modbus(module['ip'])
                if outputs[0]:
                    module['status'] = 'success'
                elif outputs[1]:
                    module['status'] = 'danger'
                elif outputs[3]:
                    module['status'] = 'info'
                elif outputs[4]:
                    module['status'] = 'warning'
                elif outputs[5]:
                    module['status'] = 'danger'


                module['latency'] = latency
                module['online'] = online

            modules_list.append(module)
        

        location['location'] = modules[0]['location']
        location['modules'] = modules_list
        module_locations.append(location)


if __name__ == '__main__':

    getAll()