from pyModbusTCP.client import ModbusClient
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


c = ModbusClient(host='172.19.246.193', port=502, auto_open=True, timeout=1)

# Read up to modbus register 60
values = c.read_holding_registers(66, 1)



for i, value in enumerate(values):

    print(f'{i+1} - {value}')


print(values[0])

print(toFloat16(values[0]))
