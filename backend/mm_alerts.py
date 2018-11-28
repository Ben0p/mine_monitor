#! /usr/bin/python3.6

import requests
from xml.etree import ElementTree
import pymongo
from bson.json_util import dumps
import json
import copy
import time
import json
from pyModbusTCP.client import ModbusClient
import subprocess, platform
import os

'''
Mine systems status board backend status polling script thing
if youAreReadingThis:
    input("How bored are you?")
'''

# Initialize mongo
client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
db = client['minemonitor']


def getDetails():
    '''
    Get array of alert objects from mongodb
    '''

    # Reset the array
    alerts = []

    alert_objects = db['alert'].find()

    # Extract location, ip and type
    for alert in alert_objects:
        # Reset the SIGN dictioary
        alert_dict = {
            'location' : '',
            'ip' : '',
            'type' : '',
            'online' : False,
            'latency' : 999, 
            'sign' : False,
            'calert' : False,
            'trailer' : False,
            'rest' : False,
            'all_clear' : False,
            'emergency' : False,
            'lightning' : False,
            'a' : False,
            'b' : False,
            'c' : False
        }
        alert_dict['location'] = alert['location']
        alert_dict['ip'] = alert['ip']
        alert_dict['type'] = alert['type']

        # Determine if 'C' Alert, Trailer or Sign
        if alert_dict['type'] == 'calert':
            alert_dict['calert'] = True
        elif alert_dict['type'] == 'trailer':
            alert_dict['trailer'] = True
        else:
            alert_dict['sign'] = True

        # Duplicate the dictionary
        my_copy = copy.deepcopy(alert_dict)
        # Append to list
        alerts.append(my_copy)
    return(alerts)

def ping(host):
    """
    Returns True and latency if host responds to a ping request
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
    '''
    Checks for active Rest API on supplied ip
    '''

    #Adam I/O controller login
    user = 'root'
    passw = '00000000'
    
    do_xml = 'http://{}/digitaloutput/all/value'.format(ip)
    with requests.Session() as session:
        try:
            response = session.get(do_xml, auth=(user, passw), timeout=1)
            # Placeholder for xml response
            ElementTree.fromstring(response.content)
            return(True)
        except:
            return(False)


def modbus(ip):
    '''
    Get output states via modbus over ip.
    '''
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


def writeDB(alert):

    # Check if collection exists
    collections = db.collection_names()
    if 'alert_data' in collections:
        existing_document = db['alert_data'].find({'location' : alert['location']})
        
        # Check if a document was returned
        if existing_document.count() == 1:
                # Update document
                db['alert_data'].find_one_and_update(
                    {
                        "location": alert['location']
                    }, 
                    {
                        "$set": {
                        'ip' : alert['ip'],
                        'type' : alert['type'],
                        'online' : alert['online'],
                        'latency' : alert['latency'], 
                        'sign' : alert['sign'],
                        'calert' : alert['calert'],
                        'trailer' : alert['trailer'],
                        'rest' : alert['rest'],
                        'all_clear' : alert['all_clear'],
                        'emergency' : alert['emergency'],
                        'lightning' : alert['lightning'],
                        'a' : alert['a'],
                        'b' : alert['b'],
                        'c' : alert['c']
                        }
                    }
                )

        # Check if there is more than one document returned
        elif existing_document.count() > 1:
                # delete duplicates and insert one
                db['alert_data'].delete_many({'location' : alert['location']})
                db['alert_data'].insert_one(dumps(alert))

        elif existing_document.count() == 0:
                # Create document
                db['alert_data'].insert_one(alert)
    else:
        db['alert_data'].insert_one(dumps(alert))


def getAll():
    '''
    Main function
    '''

    # Generate array of signs with location and IP
    alerts = getDetails()

    # For each sign...
    for alert in alerts:
        # Check if online
        online = ping(alert['ip'])
        alert['online'] = online[0]
        alert['latency'] = online[1]
        if alert['online']:
            # Check if REST API available
            alert['rest'] = restAPI(alert['ip'])
            # Get modbus outputs
            outputs = modbus(alert['ip'])
            # Set output states
            alert['all_clear'] = outputs[0]
            alert['emergency'] = outputs[1]
            alert['lightning'] = outputs[2]
            alert['a'] = outputs[3]
            alert['b'] = outputs[4]
            alert['c'] = outputs[5]

        writeDB(alert)
        # Print results
        print('{}'.format(alert['location']))
        print('--IP: {}'.format(alert['ip']))
        print('--Type: {}'.format(alert['type']))
        print('--Online: {}'.format(alert['online']))
        print('--Latency: {}ms'.format(alert['latency']))
        print('---------------')
    


    print('Sleeping for 30 sec...')
    time.sleep(30)


if __name__ == '__main__':

    while True:
        getAll()
