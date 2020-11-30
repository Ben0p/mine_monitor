from env.sol import env

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import time
import pymongo
import json
from datetime import datetime
import pytz



# Initialize mongo
CLIENT = pymongo.MongoClient(f"mongodb://{env.mongodb_ip}:{env.mongodb_port}")
DB = CLIENT[env.database]


def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return(chrome_options)


def authenticate(driver):
    ''' Connects to the aspx page and authenticates
        Returns the session
    '''
    
    # Get login page
    driver.get(env.login_url)
    time.sleep(2)
    
    # Fill out form
    driver.find_element_by_name("ctl00$MainContent$TextBoxUsername").send_keys(env.username)
    time.sleep(1)
    driver.find_element_by_name("ctl00$MainContent$TextBoxPassword").send_keys(env.password)
    time.sleep(1)
    # Submit
    driver.find_element_by_name("ctl00$MainContent$ButtonLogin").click()



def parse(report, data):
    ''' Parses data to labelled dictionary
    '''

    # Common values
    headers = data['Header']
    description = data['Description']

    results = []

    for datapoints in data['Data']:
        values = {}

        # Process time
        #2020-11-27T16:00:00Z
        timestamp = datetime.strptime(datapoints[0], '%Y-%m-%dT%H:%M:%SZ')
        timestamp.replace(tzinfo=pytz.timezone('Etc/GMT-0'))

        values['timestamp'] = timestamp
        values['description'] = description
        values['type'] = report['type']
        values['span'] = report['span']
        values['location'] = report['location']
        values['report_id'] = report['_id']

        for idx, datapoint in enumerate(datapoints):
            values[headers[idx]] = datapoint

        results.append(values)

    return(results)


def updateDB(data):


    for datapoint in data:

        DB['weather_data'].find_one_and_update(
            {
                'report_id' : datapoint['report_id'],
                'timestamp' : datapoint['timestamp'],
            },
            {
                '$set': datapoint
            },
            upsert=True
        )


def process_reports(driver):
    ''' Process a list of reports from env
    '''

    # Get list of report URLs form environment
    reports = DB['weather_reports'].find()

    for report in reports:
        driver.get(report['url'])
        time.sleep(1)
        data = driver.find_element_by_tag_name("pre")
        data = data.text
        data = json.loads(data)

        data = parse(report, data)
        updateDB(data)

        print(f"Processed {report['location']} - {report['type']} - {report['span']}")


def run():

    chrome_options = set_chrome_options()
    driver = webdriver.Chrome()

    while True:

        authenticate(driver)
        process_reports(driver)
        time.sleep(10)

    



if __name__ == "__main__":
    run()