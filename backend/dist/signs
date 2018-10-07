#! /usr/bin/python3.6

import requests
from xml.etree import ElementTree
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


def getDetails(filein):
    '''
    Parses signs_file, returns list of dictionaries with sign information.
    '''

    # Reset the array
    signs = []

    # Parse the .xml
    tree = ElementTree.parse(filein)
    # Get root of the xml
    root = tree.getroot()

    # Extract location, ip and type
    for child in root:
        # Reset the SIGN dictioary
        SIGN = {
            'LOCATION' : '',
            'IP' : '',
            'TYPE' : '',
            'ONLINE' : False,
            'LATENCY' : 999, 
            'SIGN' : False,
            'CALERT' : False,
            'TRAILER' : False,
            'REST' : False,
            'ALL_CLEAR' : False,
            'EMERGENCY' : False,
            'LIGHTNING' : False,
            'A' : False,
            'B' : False,
            'C' : False
        }
        SIGN['LOCATION'] = child[1].text
        SIGN['IP'] = child[3].text
        # Determine if 'C' Alert, Trailer or Sign
        alert = SIGN['LOCATION'].split('-')
        if len(alert) == 2:
            if alert[1] == ' C Alert':
                SIGN['TYPE'] = 'C Alert'
                SIGN['CALERT'] = True
            elif alert[0][:3] == 'TR0':
                SIGN['TYPE'] = 'Trailer'
                SIGN['TRAILER'] = True
            else:
                SIGN['TYPE'] = 'Sign'
                SIGN['SIGN'] = True
        else:
            SIGN['TYPE'] = 'Sign'
            SIGN['SIGN'] = True

        # Duplicate the dictionary
        my_copy = copy.deepcopy(SIGN)
        # Append to list
        signs.append(my_copy)
    return(signs)

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


def saveJSON(signs, fileout):
    '''
    Converts list of sign dictionaries to json
    '''
    signs_json = json.dumps(signs)
    with open(fileout, 'w') as f:
        f.write(signs_json)
        f.close()


def getAll(filein, fileout):
    '''
    Main function
    '''

    # Generate array of signs with location and IP
    signs = getDetails(filein)

    # For each sign...
    for sign in signs:
        # Check if online
        online = ping(sign['IP'])
        sign['ONLINE'] = online[0]
        sign['LATENCY'] = online[1]
        if sign['ONLINE']:
            # Check if REST API available
            sign['REST'] = restAPI(sign['IP'])
            # Get modbus outputs
            outputs = modbus(sign['IP'])
            # Set output states
            sign['ALL_CLEAR'] = outputs[0]
            sign['EMERGENCY'] = outputs[1]
            sign['LIGHTNING'] = outputs[2]
            sign['A'] = outputs[3]
            sign['B'] = outputs[4]
            sign['C'] = outputs[5]
        # Print results
        print('{}'.format(sign['LOCATION']))
        print('--IP: {}'.format(sign['IP']))
        print('--Type: {}'.format(sign['TYPE']))
        print('--Online: {}'.format(sign['ONLINE']))
        print('--Latency: {}ms'.format(sign['LATENCY']))
        print('---------------')
    
    # Convert to json and save to file
    saveJSON(signs, fileout)

    print('Sleeping for 30 sec...')
    time.sleep(30)




if __name__ == '__main__':

    if platform.system().lower()=="windows":
        # Testing file location
        signs_file = './signs.xml'
        json_file = '../../frontend/src/assets/json/signs.json'
    else:
        # Linux productin file locations
        signs_file = '/home/minesys/Desktop/signs.xml'
        json_file = '/usr/share/nginx/html/assets/json/signs.json'


    while True:
        getAll(signs_file, json_file)
