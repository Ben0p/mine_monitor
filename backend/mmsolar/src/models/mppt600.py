from env.sol import env

from pyModbusTCP.client import ModbusClient
import pymongo
import time
import numpy as np
import struct



def toFloat16(value):
    '''Converts int to 16 bit float
    '''

    value = int(value)

    b =struct.pack("H",int(value))
    result = np.frombuffer(b, dtype =np.float16)[0]
    result = result.item()
    result = "{0:.2f}".format(result)

    return(result)


def targetVoltage(target, batt):
    ''' Caclulates target voltage, accounts for night mode
    '''

    target = float(toFloat16(target))
    batt = float(toFloat16(batt))

    if target < 1:
        if batt <= 18:
            target = 12.65
            low = 11.89
        elif 18 < batt <= 30:
            target = 25.3
            low = 23.78
        elif batt >= 30:
            target = 50.6
            low = 47.56
    else:
        if batt <= 18:
            low = 11.89
        elif 18 < batt <= 30:
            low = 23.78
        elif batt >= 30:
            low = 47.56

    if batt > target:
        target = batt
    
    return(target, low)


def calcSOC(batt_volts, target, low):
    ''' Calculates the state of charge % (decimal)
    '''

    batt_volts = float(batt_volts)
    
    _range = target - low
    charge = batt_volts - low
    soc = (charge / _range) * 100
    soc = int(soc)

    return(soc)

def percentage(total, value):

    total = float(total)
    value = float(value)

    percentage = (value / total) * 100
    percentage = int(percentage)

    return(percentage)


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


def getColor(soc):
    ''' Turns percentage into color
    '''

    try:

        if soc <= 50:
            color = "danger"
        elif 50 < soc <= 80:
            color = "warning"
        elif 80 < soc:
            color = "success"
        else:
            color = "info"

    except ZeroDivisionError:
        color = "info"

    return(color)


def parse(tristar):
    '''
    Gets tristar data via modbus and writes to tristar_data db
    This function is threaded for each trailer
    '''

    # Have to create a new mongo connection for each thread or it wigs out
    client = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
    db = client[env['database']]


    while True:
        # Initialize modbus connection 
        # Inside the loop incase IP changes
        c = ModbusClient(host=tristar['ip'], port=502, auto_open=True, timeout=1)

        # Read up to modbus register 60
        values = c.read_holding_registers(0, 80)

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
                'vb_ref' : values[51],
                'power_out_shadow': values[58],
                'va_max_daily' : values[66]
            }

            # Save converted values to dictionary
            live_values = {
                'online' : True,
                'batt' : {},
                'solar' : {},
                'charge_state': chargeState(raw_values['charge_state']),
                'output_power': toFloat16(raw_values['power_out_shadow']),
                'heatsink_temp': raw_values['T_hs'],
            }
            
            # Calc values
            batt_volts = toFloat16(raw_values['adc_vb_f_med'])
            target_voltage, minimum_voltage = targetVoltage(raw_values['vb_ref'], raw_values['adc_vb_f_med'])
            soc = calcSOC(batt_volts, target_voltage, minimum_voltage)

            # Battery
            live_values['batt']['volts'] = batt_volts
            live_values['batt']['current']: toFloat16(raw_values['adc_ib_f_shadow'])
            live_values['batt']['target'] = target_voltage
            live_values['batt']['min'] = minimum_voltage
            live_values['batt']['color'] = getColor(soc)
            live_values['batt']['soc'] = soc

            # Solar
            live_values['solar']['volts'] = toFloat16(raw_values['adc_va_f'])
            live_values['solar']['current'] = toFloat16(raw_values['adc_ia_f_shadow'])
            live_values['solar']['max'] = toFloat16(raw_values['va_max_daily'])
            live_values['solar']['percentage'] = percentage(live_values['solar']['max'], live_values['solar']['volts'])
            live_values['solar']['color'] = getColor(live_values['solar']['percentage'])


        # Blank values if there is no connection
        else: 
            live_values = {
                'online' : False,
            }

        # Check for changes
        # Get name and ip from solar_controllers -> insert into solar_data
        # Update ip for polling

        try:
            controller = db['solar_controllers'].find_one(
                {
                    '_id' : tristar['_id']
                }
            )

            # Reset ip in the event it has changed
            tristar['ip'] = controller['ip']

            # Dump into tristar_data collection
            db['solar_data'].find_one_and_update(
                {
                    'controller_oid' : tristar['_id'],
                },
                {
                    '$set': {
                        'ip': controller['ip'],
                        'name': controller['name'],
                        'location': controller['location'],
                        'controller_oid' : tristar['_id'],
                        'live' : live_values
                    }
                },
                upsert=True
            )

        except:

            # Dump into tristar_data collection
            db['solar_data'].find_one_and_update(
                {
                    'controller_oid' : tristar['_id'],
                },
                {
                    '$set': {
                        'ip': tristar['ip'],
                        'name': tristar['name'],
                        'location': tristar['location'],
                        'controller_oid' : tristar['_id'],
                        'live' : live_values
                    }
                },
                upsert=True
            )

        print(f"{time.strftime('%d/%m/%Y %X')} - Polled {tristar['name']}")
        # Every 2 seconds so it doesn't go out of control
        time.sleep(5)