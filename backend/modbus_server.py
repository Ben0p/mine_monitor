#!/usr/bin/env python
# scripts/examples/simple_tcp_server.py
import logging
from socketserver import TCPServer
from collections import defaultdict

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream

# Add stream handler to logger 'uModbus'.
log_to_stream(level=logging.DEBUG)

# A very simple data store which maps addresss against their values.
data_store = defaultdict(int)

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = False

TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ('10.58.10.31', 502), RequestHandler)


@app.route(slave_ids=[x for x in range(0,9999)], function_codes=[1, 2, 3, 4], addresses=list(range(0, 25)))
def read_data_store(slave_id, function_code, address):
    """" Return value of address. """
    print(data_store)
    return data_store[address]


@app.route(slave_ids=[x for x in range(0,9999)], function_codes=[5, 6, 15, 16], addresses=list(range(0, 25)))
def write_data_store(slave_id, function_code, address, value):
    """" Set value for address. """
    print(data_store)
    data_store[address] = value

if __name__ == '__main__':
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()