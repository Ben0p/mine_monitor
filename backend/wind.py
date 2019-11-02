
from env.devprod import env
from xml.etree import ElementTree
import requests
import pymongo
from bson.json_util import dumps
import json
import copy
import time
import json
import subprocess, platform
import os


""""Wind polling script
Production and development environment variabes in env
Retrieves data from mongo db
Polls url of anemometers for xml
Writes results back in mongo
"""

# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]








if __name__ == "__main__":
    
