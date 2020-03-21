from env.sol import env

from pysnmp.hlapi import *
import sys
import time
import pymongo



# Initialize mongo
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]


def walk(host, oid):
    ''' Walks SNMP starting from oid
        Returns dictionary
    '''

    results = {}

    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                              CommunityData('public', mpModel=0),
                              UdpTransportTarget((host, 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid)),
                              ):

        if errorIndication:
            print(errorIndication, file=sys.stderr)
            break

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
            break

        else:
            oid, value = varBinds[0]
            oid = str(oid)
            value = str(value)

            if value == '1':
                value = True
            elif value == '0':
                value = False

            results[oid] = value

    return(results)




if __name__ == '__main__':

    while True:
        # Get generator IO modules details
        modules = DB['gen_modules'].find()
        
        for module in modules:

            # Get all SNMP values
            results = walk(module['ip'], '1.3.6.1.4.1.8691.10.2210')

            # Get only DI values
            di = {}
            for i in range(12):
                di[f'di_{i}'] = results[f'1.3.6.1.4.1.8691.10.2210.10.1.1.4.{i}']

            try:
                oil = di[module['oil_di']]
                # Reverse logic, activated input = not running
                if oil:
                    oil = False
            except KeyError:
                oil = None
            
            try:
                flex = di[module['flex_di']]
            except KeyError:
                flex = None
            
            try:
                fuel = di[module['fuel_di']]
            except KeyError:
                fuel = None

            
            # Insert into DB
            DB['gen_status'].find_one_and_update(
                {
                    'module_oid' : module['_id'],
                },
                {
                    '$set': {
                        'ip': module['ip'],
                        'name': module['name'],
                        'module_oid' : module['_id'],
                        'inputs' : di,
                        'oil' : oil,
                        'flex' : flex,
                        'fuel' : fuel,
                    }
                },
                upsert=True
            )

            print(f"Polled {module['name']}")
        
        time.sleep(10)