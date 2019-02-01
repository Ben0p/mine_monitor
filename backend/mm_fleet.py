#! /usr/bin/python3.6

import time
import os
import pymongo
import subprocess, platform
import multiprocessing



def get(device):
    # Have to create a new mongo connection for each thread or it wigs out
    client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
    db = client['minemonitor']

    for pong, online in ping(device['ip']):
        # Check if device hasn't been deleted
        fleet_exists = db['fleet'].find_one({"name": device['name']})
        fleet_data = db['fleet_data'].find_one({"name": device['name']})

        if fleet_exists:
            db['fleet_data'].find_one_and_update(
                {
                    "name": device['name']
                }, 
                {
                    "$set": 
                        {
                            device['device']+'Latency' : pong,
                            device['device']+'Online' : online,
                            device['device']+'IP' : device['ip']
                        }
                },
                upsert = True
            )
        
        # If it doesn't exist...
        else:
            # AND if it exists in fleet_data
            if fleet_data:
                # Delete from fleet_data
                db['fleet_data'].find_one_and_delete({"name": device['name']})



def ping(host):
    """
    Returns True and latency if host responds to a ping request
    """
    if platform.system().lower()=="windows":
        cmd = ["ping", host, "-t"]
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            if stdout_line[:5] == "Reply":
                try:
                    yield(stdout_line.split()[4].split('=')[1][:-2], True)
                except IndexError:
                    yield(999, False)
            elif stdout_line[:7] == "Request":
                yield(999, False)

        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)

    else:
                
        cmd = ['ping', host]
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            if stdout_line[:2] == "64":
                try:
                    yield(stdout_line.split()[6].split('=')[1][:-3], True)
                except IndexError:
                    yield(999, False)
            elif stdout_line[:4] == "From":
                yield(999, False)
            else:
                yield(999, False)

        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)


def main():
    # Database
    client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
    db = client['minemonitor']

    active_processes = []
    process_match = {}

    while True:
        # Get fleet documents
        docs = db['fleet'].find()

        # Reset fleet devices array for extending
        devices = []

        # Reset fleet device list for process tracking
        device_list = []
    
        # Each machine object
        for document in docs:

            # Create list of all the devices every machine
            try:
                devices.extend(
                    [
                        {
                            "name": document['name'],
                            "device": "xim",
                            "ip": document['xim']
                        },
                        {
                            "name": document['name'],
                            "device": "two",
                            "ip": document['two']
                        },
                        {
                            "name": document['name'],
                            "device": "screen",
                            "ip": document['screen']
                        },
                        {
                            "name": document['name'],
                            "device": 'ms352',
                            "ip": document['ms352']
                        }
                    ]
                )
            except:
                pass

        for device in devices:

            # Generate a unique device name (DT050-xim)
            device_name = "{}-{}".format(device['name'],device['device'])

            # Append device name to list
            device_list.append(device_name)

            # Check if there is a process already running with the device name
            if device_name not in active_processes:

                # Create process
                p = multiprocessing.Process(
                    target=get,
                    args=(device,)
                    )
                
                # Append device name to active process list
                active_processes.append(device_name)

                # Add process ID to dictionary
                process_match[device_name] = p

                # Start process
                p.start()
                print("Started {}".format(device_name))

        
        # Stop process if the fleet device has been removed from db
        for process in active_processes:
            # If there is a process running that isn't in the db
            if process not in device_list:
                # Terminate that process
                process_match[process].terminate()
                # Remove from active processes
                active_processes.remove(process)
                # Remove from process match dictionary
                del process_match[process]

                print("Stopped {}".format(process))



        time.sleep(10)





if __name__ == '__main__':
    main()