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


def modelE2210(module):
    # Get all SNMP values
    results = walk(module['ip'], '1.3.6.1.4.1.8691.10.2210')

    # Get only DI values
    di = {}
    for i in range(12):
        try:
            di[f'di_{i}'] = results[f'1.3.6.1.4.1.8691.10.2210.10.1.1.4.{i}']
        except KeyError:
            di[f'di_{i}'] = None

    try:
        oil = di[module['oil_di']]

        # Reverse logic, activated input = not running
        # Explicitly defined because None was being read as False
        if oil == True:
            oil = False
        elif oil == False:
            oil = True
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

    
    status = {
        'oil' : oil,
        'flex' : flex,
        'fuel' : fuel,
        'fuel_level' : None,
        'fuel_color' : "primary",
        'di' : di,
        'ai' : None
    }

    return(status)


def modelE2214(module):

    # Get all SNMP values
    results = walk(module['ip'], '1.3.6.1.4.1.8691.10.2214.1.0')

    # Get only DI values
    di = {}
    for i in range(5):
        try:
            di[f'di_{i}'] = results[f'1.3.6.1.4.1.8691.10.2214.10.1.1.4.{i}']
        except KeyError:
            di[f'di_{i}'] = None

    try:
        oil = di[module['oil_di']]

        # Reverse logic, activated input = not running
        # Explicitly defined because None was being read as False
        if oil == True:
            oil = False
        elif oil == False:
            oil = True
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

    
    status = {
        'oil' : oil,
        'flex' : flex,
        'fuel' : fuel,
        'fuel_level' : None,
        'fuel_color' : "primary",
        'di' : di,
        'ai' : None
    }

    return(status)


def modelE2242(module):
    # Get all SNMP values
    ''' 
    AI0:
    Start = 1.3.6.1.4.1.8691.10.2242.10.2.1
    values = 1.3.6.1.4.1.8691.10.2242.10.2.1.4
    min = 1.3.6.1.4.1.8691.10.2242.10.2.1.5
    max = 1.3.6.1.4.1.8691.10.2242.10.2.1.6

    DI0:
    start = 1.3.6.1.4.1.8691.10.2242.10.1.1.4.{i}
    '''

    # DI snmp results
    di_results = walk(module['ip'], '1.3.6.1.4.1.8691.10.2242.10.1.1.4')
    # AI snmp results
    ai_results = walk(module['ip'], '1.3.6.1.4.1.8691.10.2242.10.2.1')


    # Get DI values
    di = {}
    for i in range(5):
        try:
            di[f'di_{i}'] = di_results[f'1.3.6.1.4.1.8691.10.2242.10.1.1.4.{i}']
        except KeyError:
            di[f'di_{i}'] = None

    # Oil
    try:
        oil = di[module['oil_di']]

        # Reverse logic, activated input = not running
        # Explicitly defined because None was being read as False
        if oil == True:
            oil = False
        elif oil == False:
            oil = True
    except KeyError:
        oil = None
    
    # Flex
    try:
        flex = di[module['flex_di']]
    except KeyError:
        flex = None
    
    # Fuel 
    try:
        fuel = di[module['fuel_di']]
    except KeyError:
        fuel = None

    # Get AI values
    ai = {}
    for i in range(4):
        try:
            ai[f'ai_{i}'] = ai_results[f'1.3.6.1.4.1.8691.10.2242.10.2.1.4.{i}']
            ai[f'ai_{i}_min'] = ai_results[f'1.3.6.1.4.1.8691.10.2242.10.2.1.5.{i}']
            ai[f'ai_{i}_max'] = ai_results[f'1.3.6.1.4.1.8691.10.2242.10.2.1.6.{i}']
        except KeyError:
            ai[f'ai_{i}'] = None
            ai[f'ai_{i}_min'] = None
            ai[f'ai_{i}_max'] = None
    


    level = int(ai[module['level_ai']])
    # temp
    try:
        temp = int(ai[module['temp_ai']])
    except KeyError:
        temp = False

    # Fuel
    try:
        fuel_min = int(module['fuel_min'])
        fuel_max = int(module['fuel_max'])
    except KeyError:
        fuel_min = 1
        fuel_max = 1

    fuel_range = fuel_max - fuel_min
    fuel_level = ((level-fuel_min) / fuel_range) * 100
    fuel_level = round(fuel_level)

    if fuel_level > 100:
        fuel_level = 100
        fuel_color = "success"
    if 70 <= fuel_level <= 100:
        fuel_color = "success"
    elif 30 <= fuel_level < 70:
        fuel_color = "warning"
    elif fuel_level <= 30:
        fuel_color = "danger"

    if temp:
        temp = (((temp / 65535)*20)*1000)-273
        temp = int(temp)
    else:
        temp = 0

    status = {
        'oil' : oil,
        'flex' : flex,
        'fuel' : fuel,
        'fuel_level' : fuel_level,
        'fuel_color' : fuel_color,
        'temp' : temp,
        'di' : di,
        'ai' : ai
    }

    return(status)



if __name__ == '__main__':

    while True:
        # Get generator IO modules details
        modules = DB['gen_modules'].find()
        
        for module in modules:
            status = {
                'di' : {},
                'ai' : {},
                'oil' : None,
                'flex' : None,
                'fuel' : None
            }
            
            if module['model'] == 'E2210':
                status = modelE2210(module)
            elif module['model'] == 'E2214':
                status = modelE2214(module)
            elif module['model'] == 'E2242':
                status = modelE2242(module)
            
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
                        'di' : status['di'],
                        'ai' : status['ai'],
                        'oil' : status['oil'],
                        'flex' : status['flex'],
                        'fuel' : status['fuel'],
                        'temp' : status['temp'],
                        'fuel_level' : status['fuel_level'],
                        'fuel_color' : status['fuel_color']
                    }
                },
                upsert=True
            )

            print(f"{time.strftime('%d/%m/%Y %X')} - Polled {module['name']}")
        
        time.sleep(10)