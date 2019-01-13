#! /usr/bin/python3.6
import pymongo
import time


# Initialize mongo
client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
db = client['minemonitor']


def alerts():
    '''
    Returns percentage of alerts online (integer)
    '''

    # Get Alerts
    alerts = db['alert_data'].find()
    alert_count = alerts.count()

    # Reset online count
    online = 0

    # Count how many alerts online
    for alert in alerts:
        if alert['online']:
            online += 1
    
    # Calculate percentage online
    percent = (online / alert_count)*100

    return(int(percent))

def corrections():
    '''
    Returns percentage of corrections (integer)
    '''

    # Get Alerts
    corrections = db['correction_data'].find()

    # Extract the correction in percent
    percent = corrections[0]['in']['percent']

    return(int(percent))

def fleet():
    '''
    Returns percentage of fleet online (integer)
    '''

    # Get Fleet
    fleets = db['fleet_data'].find()
    fleet_count = fleets.count()

    # Reset online count
    online = 0

    # Count how many fleet not in failure
    for fleet in fleets:
        devices_online = sum([fleet['twoOnline'], fleet['ximOnline'], fleet['screenOnline']])
        if devices_online == 3 or devices_online == 0:
            online += 1
    
    # Calculate percentage online
    percent = (online / fleet_count)*100

    return(int(percent))



def services():
    '''
    Returns dictionary of what services are running
    And percentage of running services
    '''

    # Get Services
    services = db['services'].find()
    service_count = services.count()

    # Reset online count
    online = 0
    
    # Reset dictionary
    status = {}
    
    # Generate dictrionary and count services online
    for service in services:

        status[service['service']]  = service['running']

        if service['running']:
            online += 1

    # Calculate percentage online
    percent = (online / service_count)*100
        

    return(status, int(percent))


def trailers():
    '''
    Returns percentage of trailers online (integer)
    '''

    # Get Trailers
    trailers = db['tristar_data'].find()
    trailer_count = trailers.count()

    # Reset online count
    online = 0

    # Count how many trailers online
    for trailer in trailers:
        if trailer['live']['online']:
            online += 1
    
    # Calculate percentage online
    percent = (online / trailer_count)*100

    return(int(percent))

def writeDB(document):

    db['overview'].find_one_and_update(
        {
            'parent': 'home'
        },
        {
            '$set': document
        },
        upsert=True
    )





def main():

    # Alert percentage
    alert_percentage = alerts()

    # Corrections in percentage
    corrections_percentage = corrections()

    # Fleet percentage
    fleet_percentage = fleet()

    # Services status and percentage
    services_status, services_percentage = services()

    # Trailers percentage
    trailers_percentage = trailers()

    # Testing 
    '''
    print("Alerts: {} - {}%".format(services_status['alert'], alert_percentage))
    print("Corrections: {} - {}%".format(services_status['corrections'], corrections_percentage))
    print("Fleet: {} - {}%".format(services_status['fleet'], fleet_percentage))
    print("Services: {} - {}%".format(services_status['services'], services_percentage))
    print("Trailers: {} - {}%".format(services_status['trailers'], trailers_percentage))
    print('-----------------------------------')
    '''


    document = {
        'parent' : 'home',
        'alerts' : {
            'running' : services_status['alert'],
            'percentage' : alert_percentage
        },
        'corrections' : {
            'running' : services_status['corrections'],
            'percentage' : corrections_percentage
        },
        'fleet' : {
            'running' : services_status['fleet'],
            'percentage' : fleet_percentage
        },
        'services' : {
            'running' : services_status['services'],
            'percentage' : services_percentage
        },
        'trailers' : {
            'running' : services_status['trailers'],
            'percentage' : trailers_percentage
        }
    }

    writeDB(document)



if __name__ == '__main__':

    print('Running....')
    while True:
        main()
        time.sleep(1)