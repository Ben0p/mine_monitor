from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import time
from registers import master, holding_integers, holding_floats, system_status, output_state

class FloatModbusClient(ModbusClient):
    def read_float(self, address, number=1):
        reg_l = self.read_holding_registers(address, number * 2)
        if reg_l:
            return [utils.decode_ieee(f) for f in utils.word_list_to_long(reg_l)]
        else:
            return None


def readIntRegisters(ip):
    c = ModbusClient(host=ip, port=502, auto_open=True)
    int_registers = {}
    for key, value in holding_integers.items():
        # Read Modbus outputs
        result = c.read_holding_registers(value,1)
        int_registers[key] = result[0]
    c.close()
    return(int_registers)


def readFloatRegisters(ip):
    c = FloatModbusClient(host=ip, port=502, auto_open=True)
    float_registers = {}
    for key, value in holding_floats.items():
        # Read Modbus outputs
        result = c.read_float(value,1)
        float_registers[key] = round(result[0],2)
    c.close()
    return(float_registers)


def lookupSysStatus(c):
    status = c.read_holding_registers(holding_integers["System Status"], 1)
    status = str(status[0])
    status = system_status[status]
    return(status)


def lookupOutputState(c):
    state = c.read_holding_registers(holding_integers["Output State"], 1)
    state = str(state[0])
    state = output_state[state]
    return(state)


def getStates(master):

    # Process system status
    if master['System Status'] == "System Normal":
        master['status'] = [{
            'status' : "System Normal",
            'system_status' : 'success',
            'system_icon' : 'checkmark-circle-2-outline'
        }]
    else:
        master['status'] = [{
            'status' : master['System Status'],
            'system_status' : 'danger',
            'system_icon' : 'alert-circle-outline'
        }]


    # Process battery charge
    if master['Battery Capacity Remaining'] < 70:
        master['batt_status'] = 'danger'
        master['batt_icon'] = 'battery-outline'
    elif 70 <= master['Battery Capacity Remaining'] < 90 :
        master['batt_status'] = 'warning'
        master['batt_icon'] = 'battery-outline'
    elif 90 <= master['Battery Capacity Remaining']:
        master['batt_status'] = 'success'
        master['batt_icon'] = 'charging-outline'

    # Process temperature
    if master['Ambient Temperature'] < 25:
        master['temp_status'] = 'info'
        master['temp_icon'] = 'thermometer-minus-outline'
    elif 25 <= master['Ambient Temperature'] < 30:
        master['temp_status'] = 'warning'
        master['temp_icon'] = 'thermometer-plus-outline'
    elif 30 <= master['Ambient Temperature']:
        master['temp_status'] = 'danger'
        master['temp_icon'] = 'thermometer-plus-outline'

    # Process load
    master['load_icon'] = 'bulb-outline'
    if master['Percent Full Load'] >= 90:
        master['load_status'] = 'danger'
    elif 90 > master['Percent Full Load'] >= 70:
        master['load_status'] = 'warning'
    elif 70 > master['Percent Full Load']:
        master['load_status'] = 'success'

    # Process volts
    phases = [master['Van Input'], master['Vbn Input'], master['Vcn Input']]
    phase_states = []

    for phase in phases:
        if phase >= 260:
            phase_status = 'danger'
        elif 260 > phase >= 250:
            phase_status = 'warning'
        elif 250 > phase:
            phase_status = 'success'

        phase_state = {
            'phase_voltage' : phase,
            'phase_icon' : 'activity-outline',
            'phase_status' : phase_status
        }

        phase_states.append(phase_state)

    master['phases'] = phase_states

    return(master)


def poll(ups):

    int_registers = readIntRegisters(ups['ip'])

    float_registers = readFloatRegisters(ups['ip'])

    master = {**int_registers, **float_registers}

    master["System Status"] = system_status[str(int_registers["System Status"])]
    master["Output State"] = output_state[str(int_registers["Output State"])]
    master["load_percent"] = master["Percent Full Load"]
    master["batt_remaining"] = master["Battery Capacity Remaining"]
    master["kw_out"] = master["Output Demand KW"]
    master["temp"] = master["Ambient Temperature"]
    master = getStates(master)

    master["module_uid"] = ups['_id']

    return(master)

