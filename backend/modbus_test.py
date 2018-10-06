from pyModbusTCP.client import ModbusClient


ip = '10.20.64.220'

c = ModbusClient(host=ip, port=502, auto_open=True)

for output in range(16, 22, 1):
    response = c.write_single_coil(output, 1)
    print("Output {} {}".format(output, response))