
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