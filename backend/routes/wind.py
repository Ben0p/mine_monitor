from flask_restful import Resource, reqparse

from env.devprod import env
# from env.docker import env
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import datetime
from flask import jsonify

# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]

class wind_collect(Resource):

    def get(self, name):
        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("mac")
        parser.add_argument("name")
        parser.add_argument("directionV")
        parser.add_argument("speedV")

        args = parser.parse_args()

        DB['wind_live'].find_one_and_update(
            {
                'name':args['name']
            },
            {
                '$set': {
                    'mac' : args['mac'],
                    'name' : args['name'],
                    'direction' : args['directionV'],
                    'speed' : args['speedV'],
                }
            },
            upsert=True
        )


class wind_all(Resource):

    def get(self):

        winds = DB['wind_live'].find().sort("name", pymongo.ASCENDING)

        return(jsonify(json.loads(dumps(winds))))