from env.sol import env

from pyModbusTCP.client import ModbusClient
import pymongo
import time



def calcVolts(hi, lo, v):
    '''
    Converts raw modbus voltage value to actual volts
    '''
    v_scaling = hi + (lo/(2**16))
    volts = v*v_scaling*(2**-15)
    return(format(volts, '.2f'))


def targetVoltage(hi, lo, target, batt):
    ''' Caclulates target voltage, accounts for night mode
    '''

    target = float(calcVolts(hi, lo, target))
    batt = float(calcVolts(hi, lo, batt))

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


def calcCurrent(hi, lo, i):
    '''
    Converts raw modbus current value to actual current
    '''
    c_scaling = hi * lo
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


def getColor(soc):
    ''' Turns percentage into color
    '''

    try:

        if soc <= 75:
            color = "danger"
        elif 75 < soc <= 90:
            color = "warning"
        elif 90 < soc:
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
                'heatsink_temp': raw_values['T_hs'],
            }

            # Calc values
            batt_volts = calcVolts(
                        raw_values['V_PU_hi'],
                        raw_values['V_PU_lo'],
                        raw_values['adc_vb_f_med']
                    )
            
            target_voltage, minimum_voltage = targetVoltage(
                        raw_values['V_PU_hi'],
                        raw_values['V_PU_lo'],
                        raw_values['vb_ref'],
                        raw_values['adc_vb_f_med'],
                    )
            
            batt_current = calcCurrent(
                        raw_values['I_PU_hi'],
                        raw_values['I_PU_lo'],
                        raw_values['adc_ib_f_shadow']
                    )
            
            soc = calcSOC(
                        batt_volts,
                        target_voltage,
                        minimum_voltage
                    )
            
            solar_volts = calcVolts(
                        raw_values['V_PU_hi'],
                        raw_values['V_PU_lo'],
                        raw_values['adc_va_f']
                    )

            solar_max = calcVolts(
                        raw_values['V_PU_hi'],
                        raw_values['V_PU_lo'],
                        raw_values['va_max_daily']
                    )
            
            solar_current = calcCurrent(
                        raw_values['I_PU_hi'],
                        raw_values['I_PU_lo'],
                        raw_values['adc_ia_f_shadow']
                    )
            
            output_power  = calcPower(
                        raw_values['V_PU_hi'],
                        raw_values['V_PU_lo'],
                        raw_values['I_PU_hi'],
                        raw_values['I_PU_lo'],
                        raw_values['power_out_shadow']
                    )

            live_values['output_power'] = output_power

            # Battery
            live_values['batt']['volts'] = batt_volts
            live_values['batt']['current'] = batt_current
            live_values['batt']['target'] = target_voltage
            live_values['batt']['min'] = minimum_voltage
            live_values['batt']['color'] = getColor(soc)
            live_values['batt']['soc'] = soc

            # Solar
            live_values['solar']['volts'] = solar_volts
            live_values['solar']['current'] = solar_current
            live_values['solar']['max'] = solar_max
            live_values['solar']['percentage'] = percentage(live_values['solar']['max'], live_values['solar']['volts'])
            live_values['solar']['color'] = getColor(live_values['solar']['percentage'])


        # Blank values if there is no connection
        else: 
            live_values = {
                'online' : False,
                'batt_volts': '',
                'batt_current': '',
                'solar_volts': '',
                'solar_current': '',
                'charge_state': '',
                'batt_target' : '',
                'output_power': '',
                'heatsink_temp': '',
                'color' : 'info'
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
        time.sleep(10)