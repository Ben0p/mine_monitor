from env.sol import env
from pysnmp.hlapi import *
import time


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

            results[oid] = value

    return(results)




while True:

    results = walk("10.243.228.22", '1.3.6.1.4.1.17491.1.5.1.1.1.2')

    IAL = "1.3.6.1.4.1.17491.1.5.1.1.1.2.3"
    IAL = results[IAL]
    IAL = IAL.split()
    IAL = int(IAL[1])/-1000
    IAL = round(IAL)

    IAR = "1.3.6.1.4.1.17491.1.5.1.1.1.2.4"
    IAR = results[IAR]
    IAR = IAR.split()
    IAR = int(IAR[1])/-1000
    IAR = round(IAR)

    print(IAL)
    print(IAR)

    time.sleep(1)