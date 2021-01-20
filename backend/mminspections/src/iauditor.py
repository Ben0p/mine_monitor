from env.sol import env

import requests
import pymongo
from datetime import datetime, timedelta
import pytz


'''
Get all audits:
    https://api.safetyculture.io/audits/search?field=audit_id&field=modified_at
Specific audit
    https://api.safetyculture.io/audits/audit_2f01e3f495474e1a87cf4cce47d1710d

'''

# Set global constants (because CBF passing values around like some sort of soccer game)
# Mongo
CLIENT = pymongo.MongoClient(f"mongodb://{env.mongodb_ip}:{env.mongodb_port}")
DB = CLIENT[env.database]
# Session
S = requests.Session()
HEADERS = {"Authorization": f'Bearer {env.ia_token}'}


def getWeek():
    ''' Get the start of the work week (Sunday midnight)
    '''

    # Today
    start = datetime.now()
    # Start of work week (Monday)
    start = start - timedelta(days=start.weekday())
    # Make it midnight
    start = start.replace().replace(hour=0, minute=0, second=0, microsecond=0)
    # Convert to ISO
    start = start.isoformat()

    return(start)


def getInspections(after):
    ''' Get all inspections after (after: ISO Datetime)
    '''

    query = f"https://api.safetyculture.io/audits/search?field=audit_id&field=modified_at&modified_after={after}Z"
    
    results = S.get(query, headers = HEADERS)

    results = results.json()

    return(results)


def getInspectionDetails(inspections):
    '''
    '''
    details = []

    for inspection in inspections['audits']:
        results = S.get(f"https://api.safetyculture.io/audits/{inspection['audit_id']}", headers = HEADERS)

        results = results.json()
        results['created_at'] = datetime.strptime(results['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        results['modified_at'] = datetime.strptime(results['modified_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        details.append(results)
    
    return(details)


def updateDB(inspections):
    ''' Insert inspection details in to mongoDB
    '''

    for inspection in inspections:

        DB['ia_inspections'].find_one_and_update(
            {
                'audit_id' : inspection['audit_id'],
            },
            {
                '$set': inspection
            },
            upsert=True
        )


def run():
    ''' Main run loop
    '''

    after = getWeek()
    inspections = getInspections(after)
    inspections = getInspectionDetails(inspections)
    updateDB(inspections)





if __name__ == "__main__":
    
    run()