#! /usr/bin/python3.6
from pyModbusTCP.client import ModbusClient
import pymongo
import subprocess
import platform
import multiprocessing
import time


'''
This script is actual chaos, desperately needs to be re-written
Currently under temporary fix's
Scrapes data for the comms trailers
Gets details from mongo which has been added through the web UI
'''

# Reset arrays and dictionaries
tristar_active = []
tristar_match = {}
ping_active = []
ping_match = {}


def calcVolts(hi, lo, v):
    '''
    Converts raw modbus voltage value to actual volts
    '''
    v_scaling = hi + (lo/(2**16))
    volts = v*v_scaling*(2**-15)
    return(format(volts, '.2f'))


def calcCurrent(hi, lo, i):
    '''
    Converts raw modbus current value to actual current
    '''
    c_scaling = hi + (lo/(2**16))
    current = i*c_scaling*(2**-15)
    return(format(current, '.2f'))


def calcPower(vhi, vlo, ihi, ilo, w):
    '''
    Converts raw modbus power value to actual power
    '''
    V_PU = vhi + vlo/(2**16)
    I_PU = ihi + ilo/(2**16)
    power = w*V_PU*I_PU*(2**-17)
    return(format(power, '.2f'))


def chargeState(state):
    '''
    Matches modbus value to a charge state
    '''

    states = {
        "0": "START",
        "1": "NIGHT_CHECK",
        "2": "DISCONNECT",
        "3": "NIGHT",
        "4": "FAULT",
        "5": "MPPT",
        "6": "ABSORPTION",
        "7": "FLOAT",
        "8": "EQUALIZE",
        "9": "SLAVE"
    }

    return(states[str(state)])


def ping(host):
    """
    Returns True and latency if host responds to a ping request
    """
    if platform.system().lower() == "windows":
        cmd = ["ping", host, "-t"]
        popen = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            if stdout_line[:5] == "Reply":
                try:
                    yield(stdout_line.split()[4].split('=')[1][:-2], True)
                except IndexError:
                    yield(999, False)
            elif stdout_line[:7] == "Request":
                yield(999, False)

        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            pass

    else:

        cmd = ['ping', host]
        popen = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            if stdout_line[:2] == "64":
                try:
                    yield(stdout_line.split()[6].split('=')[1][:-3], True)
                except IndexError:
                    yield(999, False)
            elif stdout_line[:4] == "From":
                yield(999, False)
            else:
                yield(999, False)

        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)


def parsePing(device):
    # Have to create a new mongo connection for each thread or it wigs out
    client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
    db = client['minemonitor']

    for pong, online in ping(device['ip']):

        # Check if device hasn't been deleted
        trailer_exists = db['trailers'].find_one({"parent": device['name']})
        trailer_data = db['trailer_data'].find_one({"parent": device['name']})

        if trailer_exists:
            data = {
                'latency': pong,
                'online': online,
                'ip': device['ip']
            }
            

            db['trailer_data'].find_one_and_update(
                {
                    "parent": device['name']
                },
                {
                    "$set": {
                        'parent': device['name'],
                        device['device']: data
                    }
                },
                upsert=True
            )

        # If it doesn't exist...
        else:
            # AND if it exists in fleet_data
            if trailer_data:
                # Delete from fleet_data
                db['trailer_data'].find_one_and_delete(
                    {"parent": device['name']})
                print('Deleted {}'.format(device['name']))


def parseTristar(device):
    '''
    Gets tristar data via modbus and writes to trailer_data db
    This function is threaded for each trailer
    '''

    ip = device['ip']
    name = device['name']

    # Have to create a new mongo connection for each thread or it wigs out
    client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
    db = client['minemonitor']

    # Initialize modbus connection
    c = ModbusClient(host=ip, port=502, auto_open=True, timeout=1)

    #while True:

    # Read up to modbus register 60
    values = c.read_holding_registers(0, 60)

    if values:
        # Save modbus values to dictionary
        raw_values = {
            'V_PU_hi': values[0],
            'V_PU_lo': values[1],
            'I_PU_hi': values[2],
            'I_PU_lo': values[3],
            'adc_vb_f_med': values[24],
            'adc_vbterm_f': values[25],
            'adc_vbs_f': values[26],
            'adc_va_f': values[27],
            'adc_ib_f_shadow': values[28],
            'adc_ia_f_shadow': values[29],
            'T_hs': values[35],
            'charge_state': values[50],
            'power_out_shadow': values[58]
        }

        # Save converted values to dictionary
        live_values = {
            'ip': ip,
            'online': True,
            'batt_volts': calcVolts(
                raw_values['V_PU_hi'],
                raw_values['V_PU_lo'],
                raw_values['adc_vb_f_med']),
            'batt_current': calcCurrent(
                raw_values['I_PU_hi'],
                raw_values['I_PU_lo'],
                raw_values['adc_ib_f_shadow']),
            'solar_volts': calcVolts(
                raw_values['V_PU_hi'],
                raw_values['V_PU_lo'],
                raw_values['adc_va_f']),
            'solar_current': calcCurrent(
                raw_values['I_PU_hi'],
                raw_values['I_PU_lo'],
                raw_values['adc_ia_f_shadow']),
            'charge_state': chargeState(
                raw_values['charge_state']),
            'output_power': calcPower(
                raw_values['V_PU_hi'],
                raw_values['V_PU_lo'],
                raw_values['I_PU_hi'],
                raw_values['I_PU_lo'],
                raw_values['power_out_shadow']
            ),
            'heatsink_temp': raw_values['T_hs']
        }

    # Blank values if there is no connection
    else:
        live_values = {
            'ip': ip,
            'online': False,
            'batt_volts': '',
            'batt_current': '',
            'solar_volts': '',
            'solar_current': '',
            'charge_state': '',
            'output_power': '',
            'heatsink_temp': ''
        }

    # Dump into tristar_data collection
    db['trailer_data'].find_one_and_update(
        {
            'parent': name
        },
        {
            '$set': {
                'parent': name,
                'tristar_live': live_values
            }
        },
        upsert=True
    )

    # Sleep every 5 seconds, tristar crashes with too many requests
    # time.sleep(2)

def calcStats():
    client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
    db = client['minemonitor']
    collection = db['trailer_data'].find()

    device_list = ['tristar', 'tropos2', 'ubi', 'troposLAN']

    for doc in collection:

        devices_count = 0
        devices_online = 0

        for device in device_list:
            try:
                if doc[device]:
                    devices_count += 1
                    if doc[device]['online']:
                        devices_online += 1
            except:
                pass


        devices_percentage = int((devices_online / devices_count) * 100)

        devices_offline = devices_count - devices_online
        if devices_online > 0:
            online = True
        else:
            online = False
        
        # Check if gateway
        try:
            if doc['troposLAN']:
                if doc['troposLAN']['online']:
                    tropos_type = 'Gateway'
                    gateway = True
                else:
                    tropos_type = 'Node'
                    gateway = False
            else:
                troposLAN = 'Node'
        except:
            tropos_type = 'Node'
            gateway = False

        db['trailer_data'].find_one_and_update(
            {
                'parent': doc['parent']
            },
            {
                '$set': {
                    'devices_online': devices_online,
                    'devices_count' : devices_count,
                    'devices_percentage' : devices_percentage,
                    'devices_offline' : devices_offline,
                    'online' : online,
                    'tropos_type' : tropos_type,
                    'gateway' : gateway
                }
            }
        )


def generateDevices(docs):
    '''
    Generates a list of all IP devices to ping
    '''

    # Reset trailer devices array for extending
    devices = []

        
    # Iterate over docs and generate list of individual devices
    for trailer in docs:

        # Get name
        name = trailer['parent']

        # Devices to check 
        device_list = ['tropos2', 'troposLAN', 'tristar', 'ubi']

        for device in device_list:
            if trailer[device]:
                devices.append(
                    {
                        "name": name,
                        "uid": "{}-{}".format(name, device),
                        "device": device,
                        "ip": trailer[device]
                    }
                )
    
    return(devices)


def processControl(devices):
    '''
    Starts and stops processes
    '''

    # Reset tristar list
    tristar_list = []

    # For keeping track of what needs to be running
    ping_list = []


    for device in devices:

        # Check if device ip isn't blank
        if device['ip']:

            # Append device name to list
            ping_list.append(device['uid'])

            # Check if there is a process already running with the device name
            if device['uid'] not in ping_active:

                # Create process
                p = multiprocessing.Process(
                    target=parsePing,
                    args=(device,)
                )

                # Append device name to active process list
                ping_active.append(device['uid'])

                # Add process ID to dictionary
                ping_match[device['uid']] = p

                # Start process
                p.start()

                print('Started pinging {}'.format(device['uid']))
        
            if device['device'] == 'tristar':
                
                # Append device name to list
                tristar_list.append(device['uid'])

                # Check if there is a process already running with the device name
                if device['uid'] not in tristar_active:

                    # Create process
                    p = multiprocessing.Process(
                        target=parseTristar,
                        args=(device,)
                    )

                    # Append device name to active process list
                    tristar_active.append(device['uid'])

                    # Add process ID to dictionary
                    tristar_match[device['uid']] = p

                    # Start process
                    p.start()

                    print('Pythoning {}'.format(device['uid']))



    # Stop process if the device has been removed from db
    for process in ping_active:
        # If there is a process running that isn't in the db
        if process not in ping_list:
            # Terminate that process
            ping_match[process].terminate()
            # Remove from active processes
            ping_active.remove(process)
            # Remove from process match dictionary
            del ping_match[process]

            print("Stopped {}".format(process))

    # Stop process if the device has been removed from db
    for process in tristar_active:
        # If there is a process running that isn't in the db
        if process not in tristar_list:
            # Terminate that process
            tristar_match[process].terminate()
            # Remove from active processes
            tristar_active.remove(process)
            # Remove from process match dictionary
            del tristar_match[process]

            print("Stopped {}".format(process))



def main():
    '''
    Continually checks for new trailers in db and creates a new process
    '''

    # Initialize mongo
    client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
    db = client['minemonitor']


    while True:
        # Get all trailer documents
        docs = db['trailers'].find()

        # Generate list of devices
        devices = generateDevices(docs)

        # Start / stop process
        processControl(devices)

        # Calc how many devices online
        calcStats()

        time.sleep(10)


if __name__ == '__main__':
    print("Polling trailers...")
    main()
