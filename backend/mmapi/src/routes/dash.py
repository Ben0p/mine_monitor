
from env.sol import env

from flask_restful import Resource, reqparse
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
from flask import jsonify, request, Response
import datetime



# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]


def get_wind():
        module_ids = {}
        new_winds = []

        modules = DB['wind_modules'].find()
        winds = DB['wind_live'].find().sort("name", pymongo.ASCENDING)

        for module in modules:
            module_ids[module['_id']] = module

        for wind in winds:
            module_info = module_ids[wind['module_uid']]
            wind['tag'] = module_info['tag']
            wind['name'] = module_info['name']
            wind['description'] = module_info['description']
            wind['units'] = module_info['units']
            wind['type'] = module_info['type']
            new_winds.append(wind)

        return(new_winds)

class dash_power(Resource):

    def get(self):
        # Get zone list
        gen_status = DB['gen_status'].find()
        solar_data = DB['solar_data'].find()

        power_dash = {
            'gens' : gen_status,
            'solars' : solar_data
        }
        
        return(jsonify(json.loads(dumps(power_dash))))


class dash_towers(Resource):

    def get(self):
        # Get zone list
        gen_status = DB['gen_status'].find()
        solar_data = DB['solar_data'].find()
        wind_live = get_wind()

        tower_dash = {
            'gens' : gen_status,
            'solars' : solar_data,
            'winds' : wind_live
        }
        
        return(jsonify(json.loads(dumps(tower_dash))))