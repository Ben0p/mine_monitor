#! /usr/bin/python3.6
import os
import pymongo
import subprocess, platform
import time



def status(service):

        service_status = {}

        cmd = ['service', service, 'status']
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            word_list = stdout_line.split()
            try:
                first_word = word_list[0]
            except:
                continue

            if first_word == 'Active:':
                service_status['active'] = word_list[1]
                if service_status['active'] == "active":
                    service_status['running'] = True
                    service_status['status'] = word_list[2]
                    service_status['run_time'] = word_list[8]
                else:
                    service_status['running'] = False
                    service_status['status'] = word_list[1]
                    service_status['run_time'] = word_list[9]

                service_status['date'] = "{} {}".format(word_list[4], word_list[5])
                service_status['time'] = word_list[6]
                
            elif first_word == 'Main':
                service_status['pid'] = word_list[2]

        popen.stdout.close()
        return_code = popen.wait()

        if return_code:
            service_status['return_code'] = return_code
        

        return(service_status)



def main():

    # Database
    client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
    db = client['minemonitor']


    service_list = [
        'alert',
        'corrections',
        'fleet',
        'rest',
        'trailers',
        'mongod',
        'nginx',
        'services',
        'overview'
    ]

    while True:

        for service in service_list:
            service_status = status(service)
            db['services'].find_one_and_update(
                {
                    'service' : service
                },
                {
                    '$set': service_status
                },
                upsert = True
            )
        
        time.sleep(5)





if __name__ == '__main__':
    main()