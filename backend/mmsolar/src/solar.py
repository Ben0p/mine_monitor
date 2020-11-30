
from env.sol import env

from pyModbusTCP.client import ModbusClient
import pymongo
import multiprocessing
import time
import datetime

from models import mppt60, mppt600

'''
Scrapes data for the comms trailers
Gets details from mongo which has been added through the web UI
'''


def main():
    '''
    Continually checks for new MPPT Controllers and polls the modbus
    '''

    # Initialize mongo
    client = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
    db = client[env['database']]

    active_processes = []
    process_match = {}

    while True:
        # Get tristar documents
        docs = db['solar_controllers'].find()

        # Reset list of tristars in db
        tristar_list = []

        for tristar in docs:

            # Get OID
            oid = tristar['_id']

            # Append name to list
            tristar_list.append(oid)

            # Check if parent name is in active processes
            if oid not in active_processes:

                if tristar['model'] == "Tristar-60 MPPT":
                    # Create process
                    p = multiprocessing.Process(
                        target=mppt60.parse, args=(tristar,))
                elif tristar['model'] == "Tristar MPPT 600V":
                    # Create process
                    p = multiprocessing.Process(
                        target=mppt600.parse, args=(tristar,))

                # Append name to active process list
                active_processes.append(oid)

                # Add process ID to dictionary
                process_match[oid] = p

                # Start process
                p.start()

                print(f"{time.strftime('%d/%m/%Y %X')} - Started {oid}")

        # Stop process if the tristar has been removed from db
        for process in active_processes:
            # If there is a process running that isn't in the db
            if process not in tristar_list:
                # Terminate that process
                process_match[process].terminate()
                # Remove from active processes
                active_processes.remove(process)
                # Remove from process match dictionary
                del process_match[process]

                print(f"{time.strftime('%d/%m/%Y %X')} - Stopped {oid}")


        time.sleep(10)


if __name__ == '__main__':
    main()