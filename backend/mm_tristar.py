from pyModbusTCP.client import ModbusClient
import pymongo
import multiprocessing
import time


'''
In development
'''


def calcVolts(hi, lo, v):
    '''
    Converts raw modbus voltage value to actual volts
    '''
    v_scaling = hi + lo/(2**16)
    volts = v*v_scaling*2**-15
    return(format(volts, '.2f'))


def calcCurrent(hi, lo, i):
    '''
    Converts raw modbus current value to actual current
    '''
    c_scaling = hi + lo/(2**16)
    current = i*c_scaling*2**-15
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


def parseTristar(tristar):
    '''
    Gets tristar data via modbus and writes to tristar_data db
    '''

    # Have to create a new mongo connection for each thread or it wigs out
    client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
    db = client['minemonitor']

    # Initialize modbus connection
    c = ModbusClient(host=tristar['ip'], port=502, auto_open=True, timeout=1)

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
            'online' : True,
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
            )
        }

    else: 
        live_values = {
            'online' : False,
            'batt_volts': '',
            'batt_current': '',
            'solar_volts': '',
            'solar_current': '',
            'charge_state': '',
            'output_power': ''
        }

    db['tristar_data'].find_one_and_update(
        {
            'parent': tristar['parent']
        },
        {
            '$set': {
                'ip': tristar['ip'],
                'parent': tristar['parent'],
                'live' : live_values
            }
        },
        upsert=True
    )


def main():
    '''
    Continually checks for new tristars in db and creates a process
    '''

    # Initialize mongo
    client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
    db = client['minemonitor']

    active_processes = []
    process_match = {}

    while True:
        # Get tristar documents
        ts_docs = db['tristar'].find()

        # Reset list of tristars in db
        tristar_list = []

        for tristar in ts_docs:

            # Get name
            name = tristar['parent']

            # Append name to list
            tristar_list.append(name)

            # Check if parent name is in active processes
            if name not in active_processes:

                # Create process
                p = multiprocessing.Process(
                    target=parseTristar, args=(tristar,))

                # Append name to active process list
                active_processes.append(name)

                # Add process ID to dictionary
                process_match[name] = p

                # Start process
                p.start()

                print("Started {}".format(name))

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

        time.sleep(10)
        print('Sleep 10 sec')


if __name__ == '__main__':
    main()
