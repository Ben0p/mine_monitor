#! /usr/bin/python3.6
from pyModbusTCP.client import ModbusClient
import pymongo
import subprocess
import platform
import multiprocessing
import time


'''
This script is actual chaos
Currently under temporary fix's
Scrapes data for the comms trailers
Gets details from mongo which has been added through the web UI
'''


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
            raise subprocess.CalledProcessError(return_code, cmd)

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


def parseTristar(name, ip):
    '''
    Gets tristar data via modbus and writes to tristar_data db
    This function is threaded for each trailer
    '''

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

    device_list = ['cisco', 'tristar', 'tropos', 'ubi']

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
                    'online' : online
                }
            }
        )


def main():
    '''
    Continually checks for new trailers in db and creates a new process
    '''

    # Initialize mongo
    client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
    db = client['minemonitor']

    # Reset arrays and dictionaries
    active_processes = []
    process_match = {}
    active_pings = []
    ping_match = {}

    while True:
        # Get trailer documents
        docs = db['trailers'].find()

        # Reset tristar list
        tristar_list = []

        # Reset ping list
        ping_list = []

        # Reset trailer devices array for extending
        devices = []

        for trailer in docs:

            # Get name
            name = trailer['parent']

            # Append name to tristar list
            tristar_list.append(name)

            # Create list of all the devices every trailer
            try:
                devices.extend(
                    [
                        {
                            "name": name,
                            "device": "tropos",
                            "ip": trailer['tropos2_ip']
                        },
                        {
                            "name": name,
                            "device": "tristar",
                            "ip": trailer['tristar_ip']
                        },
                        {
                            "name": name,
                            "device": "cisco",
                            "ip": trailer['cisco1572_ip']
                        },
                        {
                            "name": name,
                            "device": "ubi",
                            "ip": trailer['ubi_ip']
                        }
                    ]
                )

            except:
                pass

            # Parse tristar if there is one
            if trailer['tristar_ip']:
                parseTristar(name, trailer['tristar_ip'])


        for device in devices:

            # Check if device ip isn't blank
            if device['ip']:
                # Generate a unique device name (DT050-xim)
                device_name = "{}-{}".format(device['name'], device['device'])

                # Append device name to list
                ping_list.append(device_name)

                # Check if there is a process already running with the device name
                if device_name not in active_pings:

                    # Create process
                    p = multiprocessing.Process(
                        target=parsePing,
                        args=(device,)
                    )

                    # Append device name to active process list
                    active_pings.append(device_name)

                    # Add process ID to dictionary
                    ping_match[device_name] = p

                    # Start process
                    p.start()

                    print('Started pinging {}'.format(device_name))

        # Stop process if the fleet device has been removed from db
        for process in active_pings:
            # If there is a process running that isn't in the db
            if process not in ping_list:
                # Terminate that process
                ping_match[process].terminate()
                # Remove from active processes
                active_processes.remove(process)
                # Remove from process match dictionary
                del process_match[process]

                print("Stopped {}".format(process))

        # mongo can't handle concurrent updates on the same document
        '''
        for name in tristar_list:
            # Check if tristar in active processes
            if name not in active_processes:

                # Create process
                p = multiprocessing.Process(
                    target=parseTristar, args=(name, trailer['tristar_ip'],))

                # Append name to active process list
                active_processes.append(name)

                # Add process ID to dictionary
                process_match[name] = p

                # Start process
                p.start()

                print("Pythoning {} tristar data".format(name))

        # Stop process if the tristar has been removed from db
        for process in active_processes:
            # If there is a process running that isn't in the db
            if process not in tristar_list:
                # Terminate that process
                process_match[process].terminate()
                # Remove from active processes
                active_processes.remove(process)
                # Remove from process match dictionary
                del process_match[process]

                print("Stopped {}".format(name))
        '''

        # Calc how many devices online
        calcStats()

        time.sleep(10)


if __name__ == '__main__':
    print("Polling trailers...")
    main()
