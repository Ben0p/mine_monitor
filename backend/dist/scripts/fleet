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
            }
        )


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

    documents = db['fleet'].find()

    devices = []
    
    # A little lesson in trickery
    for document in documents:
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
                        "device": "five",
                        "ip": document['five']
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


    # Set multiprocessing
    print("Pinging {} devices...".format(len(devices)))
    for device in devices:
        p = multiprocessing.Process(target=get, args=(device,))
        p.start()
        print('Pinging {} - {}'.format(device['name'], device['device']))
    print('After start')







if __name__ == '__main__':
    main()