#!/usr/bin/env python
# scripts/examples/simple_tcp_client.py
import socket

from umodbus import conf
from umodbus.client import tcp

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('10.58.10.31', 502))

# Returns a message or Application Data Unit (ADU) specific for doing
# Modbus TCP/IP.
#message = tcp.write_multiple_coils(slave_id=1, starting_address=16, values=[1, 0, 1, 1, 0, 1])

message = tcp.read_coils(slave_id=0, starting_address=16, quantity=6)

# Response depends on Modbus function code. This particular returns the
# amount of coils written, in this case it is.
response = tcp.send_message(message, sock)

print(response)

sock.close()