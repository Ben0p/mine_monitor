from env.sol import env

import wmi
import pymongo
from collectors import thumbnail, settings, summary, storage, processor



CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}")
DB = CLIENT[env['database']]


def connect(hostname):
    ''' Establishes a WMI connection to a windows Hyper-V Host
    '''
    conn = wmi.connect_server(
            server=hostname,
            user=env['wmi_user'],
            password=env['wmi_pass'],
            namespace=r"root\virtualization\v2"
        )
    client = wmi.WMI(wmi=conn)
    return(client)


def updateDBHosts(host):

    processors = host['processors']

    DB['server_data'].find_one_and_update(
        {
            'SystemName': processors['SystemName'],
        },
        {
            '$set': processors
        },
        upsert=True
    )


def run():
    ''' Main run loop
    '''

    # Get host names
    # TODO

    # Establish Connection
    client = connect('SOLHV01-01')

    # Process settings information (returns list of vm paths)
    vm_paths = settings.process(client, DB)

    # Process summary information (returns thumnail raw data)
    vm_thumbnails = summary.process(client, DB, vm_paths)

    # Process and save thumbnail image
    thumbnail.process(vm_thumbnails)

    # Process processor information
    processor.process(client, DB)




if __name__ == "__main__":
    run()