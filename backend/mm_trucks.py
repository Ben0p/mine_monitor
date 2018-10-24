import copy
import time
import json
import subprocess, platform
import os
import bs4 as bs
import requests
import utm
from multiprocessing import Pool



truckArray = json.load(open('trucks.json'))


def getData(name):
    for truck in truckArray:
        if truck['name'] == name:
            truckInfo = truck

    ximOnline, ximLatency = ping(truckInfo['xim'])
    screenOnline, screenLatency = ping(truckInfo['screen'])
    ms952Online, ms952Latency = ping(truckInfo['ms352'])
    fiveOnline, fiveLatency = ping(truckInfo['5.0'])
    twoOnline, twoLatency = ping(truckInfo['2.4'])

    if all([twoOnline, ximOnline, screenOnline]):
        allOnline = True
    else:
        allOnline = False

    truckData = {
        'name' : name,
        'allOnline' : allOnline,
        'ximOnline' : ximOnline,
        'ximLatency' : ximLatency,
        'screenOnline' : screenOnline,
        'screenLatency' : screenLatency,
        'ms952Online' : ms952Online,
        'ms952Latency' : ms952Latency,
        'fiveOnline' : fiveOnline,
        'fiveLatency' : fiveLatency,
        'twoOnline' : twoOnline,
        'twoLatency' : twoLatency
    }

    if ximOnline:
        ximInfo = scrapeXim(truckInfo['xim'])
        truckData.update(ximInfo)
    

    truckJson = json.dumps(truckData)
    return(truckJson)


def scrapeXim(ip):
    url = ''.join(['http://', ip, ':3785/getinfocore'])

    utmnum = 50
    utmlet = 'K'

    resp = requests.get(url, timeout=1)
    soup = bs.BeautifulSoup(resp.text, 'lxml')

    easting = soup.find("td", text='Easting (m):').find_next_sibling('td').text
    northing = soup.find("td", text='Northing (m):').find_next_sibling('td').text
    latlon = utm.to_latlon(float(easting),float(northing),utmnum,utmlet)

    ximinfo = {
        'device' : soup.find("td", text='Device ID:').find_next_sibling('td').text,
        'elevation' : soup.find("td", text='Elevation (m):').find_next_sibling('td').text,
        'uptime' : soup.find("td", text='Uptime Hours:').find_next_sibling('td').text,
        'one' : soup.find("td", text='Availability (1 Min.):').find_next_sibling('td').text,
        'ten' : soup.find("td", text='Availability (10 Min.):').find_next_sibling('td').text,
        'sixty' : soup.find("td", text='Availability (60 Min.):').find_next_sibling('td').text,
        'satellites' : soup.find("td", text='Satellite Count:').find_next_sibling('td').text,
        'vims' : soup.find("td", text='VIMS Communication Established:').find_next_sibling('td').text,
        'version' : soup.find("td", text='VIMS Source Version: ').find_next_sibling('td').text,
        'lat' : latlon[0],
        'lon' : latlon[1],
    }


    return(ximinfo)


def ping(host):
    """
    Returns True and latency if host responds to a ping request
    """
    if platform.system().lower()=="windows":

        try:
            response = subprocess.check_output(
                ['ping', '-n', '1', host],
                stderr=subprocess.STDOUT,  # get all output
                universal_newlines=True,  # return string not bytes
                shell=False
            )
            latencies = response.splitlines()[7]
            latency = latencies.split('=')[3][1]
            result = True
        except subprocess.CalledProcessError:
            latency = 999
            result = False
    else:
        try:
            response = subprocess.check_output(
                ['ping', '-c', '1', host]
            )
            latencies = response.splitlines()[5]
            latency = latencies.decode().split('/')[4][0]
            result = True
        except subprocess.CalledProcessError:
            latency = 999
            result = False

    return(result, latency)



def main():
    '''
    Main
    '''

    truckData = []
    how_many = len(truckArray)
    p = Pool(processes=how_many)
    results = [p.apply_async(getData, args=(truck['name'],)) for truck in truckArray]
    output = [p.get() for p in results]
    for result in output:
        truckData.append(json.loads(json.dumps(result)))
    print(truckData)

  


if __name__ == '__main__':
    main()