
from pysnmp.hlapi import *
import sys


def walk(host, oid):
    ''' Walks SNMP starting from oid
        Returns dictionary
    '''

    results = {}

    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                              CommunityData('m4DDt6ca', mpModel=0),
                              UdpTransportTarget((host, 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid)),
                              lookupMib=False,
                              lexicographicMode=False
                              ):

        if errorIndication:
            print(errorIndication, file=sys.stderr)
            return(False)

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'), file=sys.stderr)
            return(False)

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


def getData(ups):
    # Get all SNMP values
    ''' 
    Inputs:
        Start: 1.3.6.1.2.1.33.1
            Battery Charge %: 1.3.6.1.2.1.33.1.2.4.0
            Input Voltage:    1.3.6.1.2.1.33.1.3.3.1.3.1
    
    Outputs:
        Start: 1.3.6.1.4.1.534.1.4
            Load %:    1.3.6.1.4.1.534.1.4.1.0
            Watts Out: 1.3.6.1.4.1.534.1.4.4.1.4.1

    Environmental
        Start: 1.3.6.1.4.1.705.1.8
            Temp:     1.3.6.1.4.1.705.1.8.1.0
            Humidity: 1.3.6.1.4.1.705.1.8.2.0
    '''

    ups_data = {
        'online' : False,
        'batt_remaining' : 0,
        'load_percent' : 0,
        'volts_in' : 0,
        'kw_out' : 0,
        'temp' : 0,
        'module_uid' : ups['_id']
    }

    try:
        # Battery %
        batt_remaining = walk(ups['ip'], '1.3.6.1.2.1.33.1.2.4')

        # If online:
        if batt_remaining:
            # Input
            volts_in = walk(ups['ip'], '1.3.6.1.2.1.33.1.3.3.1.3')
            # Output
            load_percent = walk(ups['ip'], '1.3.6.1.4.1.534.1.4.1')
            kw_out = walk(ups['ip'], '1.3.6.1.4.1.534.1.4.4.1.4')
            # Environmental results
            temp = walk(ups['ip'], '1.3.6.1.4.1.705.1.8.1')

        # Get values

            ups_data = {
                'online' : True,
                'batt_remaining' : int(batt_remaining[f'1.3.6.1.2.1.33.1.2.4.0']),
                'volts_in' : int(volts_in[f'1.3.6.1.2.1.33.1.3.3.1.3.1']),
                'load_percent' : int(load_percent[f'1.3.6.1.4.1.534.1.4.1.0']),
                'kw_out' : int(kw_out[f'1.3.6.1.4.1.534.1.4.4.1.4.1']) / 1000,
                'temp' : int(temp[f'1.3.6.1.4.1.705.1.8.1.0']) / 10,
                'module_uid' : ups['_id']
            }
    except:
        print("Failed to process values")


    return(ups_data)


def getStates(ups):

    system_statuses = []
    error = False

    # Process system status
    if ups['volts_in'] < 200:
        error = True
        system_statuses.append({
            'status' :"Power Loss",
            'system_status' : 'danger',
            'system_icon' : 'alert-circle-outline'
        })
    if ups['volts_in'] > 260:
        error = True
        system_statuses.append({
            'status' : "Excessive Input Volts",
            'system_status' : 'danger',
            'system_icon' : 'alert-circle-outline'
        })
    if ups['batt_remaining'] < 70:
        error = True
        system_statuses.append({
            'status' : "Low Battery",
            'system_status' : 'warning',
            'system_icon' : 'alert-circle-outline'
        })
    if ups['temp'] > 30:
        error = True
        system_statuses.append({
            'status' : "High Temp",
            'system_status' : 'danger',
            'system_icon' : 'alert-circle-outline'
        })


    if not error:
        system_statuses.append({
            'status' : "System Normal",
            'system_status' : 'success',
            'system_icon' : 'checkmark-circle-2-outline'
        })

    ups['status'] = system_statuses

    # Process battery charge
    if ups['batt_remaining'] < 70:
        ups['batt_status'] = 'danger'
        ups['batt_icon'] = 'battery-outline'
    elif 70 <= ups['batt_remaining'] < 90 :
        ups['batt_status'] = 'warning'
        ups['batt_icon'] = 'battery-outline'
    elif 90 <= ups['batt_remaining']:
        ups['batt_status'] = 'success'
        ups['batt_icon'] = 'charging-outline'

    # Process temperature
    if ups['temp'] < 25:
        ups['temp_status'] = 'info'
        ups['temp_icon'] = 'thermometer-minus-outline'
    elif 25 <= ups['temp'] < 30:
        ups['temp_status'] = 'warning'
        ups['temp_icon'] = 'thermometer-plus-outline'
    elif 30 <= ups['temp']:
        ups['temp_status'] = 'danger'
        ups['temp_icon'] = 'thermometer-plus-outline'

    # Process load
    ups['load_icon'] = 'bulb-outline'
    if ups['load_percent'] >= 90:
        ups['load_status'] = 'danger'
    elif 90 > ups['load_percent'] >= 70:
        ups['load_status'] = 'warning'
    elif 70 > ups['load_percent']:
        ups['load_status'] = 'success'

    # Process volts
    phases = [ups['volts_in']]
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

    ups['phases'] = phase_states

    return(ups)


def offlineStates(ups):

    ups['status'] = [{
        'status' : "Offline",
        'system_status' : 'danger',
        'system_icon' : 'alert-circle-outline'
    }]
    ups['batt_status'] = 'basic'
    ups['batt_icon'] = 'battery-outline'
    ups['temp_status'] = 'basic'
    ups['temp_icon'] = 'thermometer-outline'
    ups['load_status'] = 'basic'
    ups['load_icon'] = 'bulb-outline'

    ups['phases'] = [{
            'phase_voltage' : 0,
            'phase_icon' : 'activity-outline',
            'phase_status' : 'basic'
        }]
    

    return(ups)



def poll(ups):

    ups_data = getData(ups)
    if ups_data['online']:
        ups_data = getStates(ups_data)
    else:
        ups_data = offlineStates(ups_data)

    return(ups_data)