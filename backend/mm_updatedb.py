import pymongo
import json


# Initialize mongodb
client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
db = client['minemonitor']




def fleet(fleet_json):
        '''
        Generates fleet collection in mongo from the input json
        '''
        # Load json
        fleetArray = json.load(open(fleet_json))
        # Get array of collection names from mongodb
        collections = db.collection_names()

        # Check if fleet collection exists
        if 'fleet' in collections:
                # For each machine in the fleet json
                for fleet in fleetArray:
                        # Return document with matching machine name, blank if none
                        existing_document = db['fleet'].find({'name' : fleet['name']})
                        # Check if a document was returned
                        if existing_document.count() == 1:
                                # Update document
                                db['fleet'].find_one_and_update(
                                        {
                                                "name": fleet['name']
                                        },
                                        {
                                                "$set": {
                                                        "xim": fleet['xim'],
                                                        "screen": fleet['screen'],
                                                        "ms352": fleet['ms352'],
                                                        "five": fleet['five'],
                                                        "two": fleet['two']    
                                                }
                                        }
         
                                )
                                print('Update {}'.format(fleet['name']))
                        # Check if there is more than one document returned
                        elif existing_document.count() > 1:
                                # Print offending document name
                                print('Duplicate name {}'.format(fleet['name']))
                                print('Deleting and recreating {}'.format(fleet['name']))
                                db['fleet'].delete_many({'name' : fleet['name']})
                                db['fleet'].insert_one(fleet)

                        elif existing_document.count() == 0:
                                # Create document
                                db['fleet'].insert_one(fleet)
                                print('Created new {}'.format(fleet['name']))

        # If fleet collection doesn't exist
        else:
                # Insert entire thing in one hit (nice)
                db['fleet'].insert_many(fleetArray)
        
        print('Processed {} records'.format(db['fleet'].find().count()))


def fleet_data(fleet_json):
        '''
        Generates fleet_data collection in mongo from the input json
        '''
        # Load json
        fleetArray = json.load(open(fleet_json))
        # Get array of collection names from mongodb
        collections = db.collection_names()
         # Check if fleet collection exists
        if 'fleet_data' in collections:
                # For each machine in the fleet json
                for fleet in fleetArray:
                        # Return document with matching machine name, blank if none
                        existing_document = db['fleet_data'].find({'name' : fleet['name']})
                        # Check if a document was returned
                        if existing_document.count() == 1:
                                # Update document
                                db['fleet'].find_one_and_update(
                                        {
                                                "name": fleet['name']
                                        },
                                        {
                                                "$set": {
                                                        "ximOnline": False,
                                                        "ximLatency": 999,
                                                        "screenOnline":False,
                                                        "screenLatency": 999,
                                                        "ms352Online": False,
                                                        "ms352Latency": 999,
                                                        "fiveOnline": False,
                                                        "fiveLatency": 999,
                                                        "twoOnline": False,
                                                        "twoLatency": 999
                                                }
                                        }
         
                                )
                                print('Update {}'.format(fleet['name']))
                        # Check if there is more than one document returned
                        elif existing_document.count() > 1:
                                # Print offending document name
                                print('Duplicate name {}'.format(fleet['name']))
                                print('Deleting and recreating {}'.format(fleet['name']))
                                db['fleet_data'].delete_many({'name' : fleet['name']})
                                db['fleet_data'].insert_one(fleet)

                        elif existing_document.count() == 0:
                                # Create document
                                db['fleet_data'].insert_one(fleet)
                                print('Created new {}'.format(fleet['name']))

        # If fleet collection doesn't exist
        else:
 
                for fleet in fleetArray:
                        db['fleet_data'].insert_one(
                                {
                                        "name": fleet['name'],
                                        "ximOnline": False,
                                        "ximLatency": 999,
                                        "screenOnline": False,
                                        "screenLatency": 999,
                                        "ms352Online": False,
                                        "ms352Latency": 999,
                                        "fiveOnline": False,
                                        "fiveLatency": 999,
                                        "twoOnline": False,
                                        "twoLatency": 999
                                }
                        )
        
        print('Processed {} records'.format(db['fleet_data'].find().count()))



def main():
        fleet('fleet.json')
        fleet_data('fleet.json')



if __name__ == '__main__':
    main()