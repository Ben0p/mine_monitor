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

    # Retrieve objects from alert collection
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

        # Reset trailer dictionary
        trailer_dict = {
            'area' : '',
            'ip' : '',
            'online' : False,
            'latency' : 999, 
            'rest' : False,
            'all_clear' : False,
            'emergency' : False,
            'lightning' : False,
            'a' : False,
            'b' : False,
            'c' : False
        }


        # Set location and type
        alert_dict['location'] = alert['location']
        alert_dict['type'] = alert['type']

        # Determine if 'C' Alert, Trailer or Sign
        if alert_dict['type'] == 'calert':
            alert_dict['calert'] = True
            alert_dict['ip'] = alert['ip']
        elif alert_dict['type'] == 'trailer':
            # Create a copy of the trailer dictionary for each area
            trailer_west = copy.deepcopy(trailer_dict)
            trailer_central = copy.deepcopy(trailer_dict)
            trailer_east = copy.deepcopy(trailer_dict)

            # Set ip's for each trailer area
            trailer_west['ip'] = alert['west_ip']
            trailer_central['ip'] = alert['central_ip']
            trailer_east['ip'] = alert['east_ip']

            # Set each area name
            trailer_west['area'] = 'West'
            trailer_central['area'] = 'Central'
            trailer_east['area'] = 'East'

            # Set trailer to true
            alert_dict['trailer'] = True

            # Append array to main dictionary
            alert_dict['areas'] = [trailer_west, trailer_central, trailer_east]

        else:
            alert_dict['sign'] = True
            alert_dict['ip'] = alert['ip']

        # Duplicate the dictionary (doesn't work if you don't do this)
        my_copy = copy.deepcopy(alert_dict)
        # Append dictionary to list of dictionaries
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
            if alert['type'] == 'trailer':
                                # Update document
                db['alert_data'].find_one_and_update(
                    {
                        "location": alert['location']
                    }, 
                    {
                        "$set": {
                            "location": alert['location'],
                            "type": alert['type'],
                            "online": alert['online'],
                            "sign": alert['sign'],
                            "calert": alert['calert'],
                            "trailer": alert['trailer'],
                            "areas": [
                                {
                                    "area": alert['areas'][0]['area'],
                                    "ip": alert['areas'][0]['ip'],
                                    "online": alert['areas'][0]['online'],
                                    "latency": alert['areas'][0]['latency'],
                                    "rest": alert['areas'][0]['rest'],
                                    "all_clear": alert['areas'][0]['all_clear'],
                                    "emergency": alert['areas'][0]['emergency'],
                                    "lightning": alert['areas'][0]['lightning'],
                                    "a": alert['areas'][0]['a'],
                                    "b": alert['areas'][0]['b'],
                                    "c": alert['areas'][0]['c'],
                                },
                                {
                                     "area": alert['areas'][1]['area'],
                                    "ip": alert['areas'][1]['ip'],
                                    "online": alert['areas'][1]['online'],
                                    "latency": alert['areas'][1]['latency'],
                                    "rest": alert['areas'][1]['rest'],
                                    "all_clear": alert['areas'][1]['all_clear'],
                                    "emergency": alert['areas'][1]['emergency'],
                                    "lightning": alert['areas'][1]['lightning'],
                                    "a": alert['areas'][1]['a'],
                                    "b": alert['areas'][1]['b'],
                                    "c": alert['areas'][1]['c'],
                                },
                                {
                                    "area": alert['areas'][2]['area'],
                                    "ip": alert['areas'][2]['ip'],
                                    "online": alert['areas'][2]['online'],
                                    "latency": alert['areas'][2]['latency'],
                                    "rest": alert['areas'][2]['rest'],
                                    "all_clear": alert['areas'][2]['all_clear'],
                                    "emergency": alert['areas'][2]['emergency'],
                                    "lightning": alert['areas'][2]['lightning'],
                                    "a": alert['areas'][2]['a'],
                                    "b": alert['areas'][2]['b'],
                                    "c": alert['areas'][2]['c'],
                                }
                            ]
                        }
                    }
                )
    
            else:
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

    # If collection doens't exist, insert entire thing
    else:
        db['alert_data'].insert_one(alert)


def getAll():
    '''
    Main function
    '''

    # Generate array of signs with location and IP
    alerts = getDetails()

    # For each sign...
    for alert in alerts:

        # If a trailer
        if alert['type'] == 'trailer':
            # For each area in trailer array
            for area in alert['areas']:
                online = ping(area['ip'])
                area['online'] = online[0]
                area['latency'] = online[1]
                if area['online']:
                    # Check if REST API available
                    area['rest'] = restAPI(area['ip'])
                    # Get modbus outputs
                    outputs = modbus(area['ip'])
                    # Set output states
                    area['all_clear'] = outputs[0]
                    area['emergency'] = outputs[1]
                    area['lightning'] = outputs[2]
                    area['a'] = outputs[3]
                    area['b'] = outputs[4]
                    area['c'] = outputs[5]
                    alert['online'] = True
        else:
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

    # Sleep for 1 sec to avoid chaos
    time.sleep(1)


if __name__ == '__main__':

    while True:
        getAll()
