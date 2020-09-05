from env.sol import env

from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import pymongo
import time
from registers import master, holding_integers, holding_floats, system_status, output_state


# Initialize mongo
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]


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


def getUPSs():

    modules = DB['ups_modules'].find()
    return(modules)


def updateDB(ups):

    DB['ups_data'].insert_one(
        {
            'module_uid' : ups['module_uid'],
            "unix" : ups['unix'],
            "status" : ups['System Status'],
            "state" : ups['Output State'],
            "van_in" : ups['Van Input'],
            "vbn_in" : ups['Vbn Input'],
            "vcn_in" : ups['Vcn Input'],
            "batt_volts" : ups['Battery Voltage'],
            "va_out" : ups['VA Out'],
            "load_precent" : ups['Percent Full Load'],
            "pf_out" : ups['Output PF'],
            "batt_remaining" : ups['Battery Capacity Remaining'],
            "kw_out" : ups['Output Demand KW'],
            "temp" : ups['Ambient Temperature']
        }
    )



def poll():

    while True:
        upss = getUPSs()

        for ups in upss:

            print(f"Polling: {ups['name']}")

            int_registers = readIntRegisters(ups['ip'])

            float_registers = readFloatRegisters(ups['ip'])

            master = {**int_registers, **float_registers}

            master["System Status"] = system_status[str(int_registers["System Status"])]
            master["Output State"] = output_state[str(int_registers["Output State"])]
            master["module_uid"] = ups['_id']
            master["unix"] = time.time()

            updateDB(master)
        
        print("Sleep 10sec")
        time.sleep(10)

        
if __name__ == "__main__":

    poll()
    

