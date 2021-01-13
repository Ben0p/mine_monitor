from env.sol import env

import requests
import pymongo


'''
Get all audits:
    https://api.safetyculture.io/audits/search?field=audit_id&field=modified_at
Specific audit
    https://api.safetyculture.io/audits/audit_2f01e3f495474e1a87cf4cce47d1710d

'''

s = requests.Session()
headers = {"Authorization": f'Bearer {env.ia_token}'}

results = s.get("https://api.safetyculture.io/audits/search?field=audit_id&field=modified_at", headers = headers)
results = results.json()

CLIENT = pymongo.MongoClient(f"mongodb://{env.mongodb_ip}:{env.mongodb_port}")
DB = CLIENT[env.database]


for result in results['audits']:


    DB['ia_inspections'].find_one_and_update(
        {
            'audit_id' : result['audit_id'],
        },
        {
            '$set': result
        },
        upsert=True
    )
