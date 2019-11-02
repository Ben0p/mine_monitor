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

def windDirection(deg):
    deg = float(deg)
    direction = 'N'
    
    if deg >= 349 and deg <= 11:
        direction = 'N'
    elif deg >= 12 and deg <= 33:
        direction = 'NNE'
    elif deg >= 34 and deg <= 56:
        direction = 'NE'
    elif deg >= 57 and deg <= 78:
        direction = 'ENE'
    elif deg >= 79 and deg <= 101:
        direction = 'E'
    elif deg >= 102 and deg <= 123:
        direction = 'ESE'
    elif deg >= 124 and deg <= 146:
        direction = 'SE'
    elif deg >= 147 and deg <= 168:
        direction = 'SSE'
    elif deg >= 169 and deg <= 191:
        direction = 'S'
    elif deg >= 192 and deg <= 213:
        direction = 'SSW'
    elif deg >= 214 and deg <= 236:
        direction = 'SW'
    elif deg >= 237 and deg <= 258:
        direction = 'WSW'
    elif deg >= 259 and deg <= 281:
        direction = 'W'
    elif deg >= 282 and deg <= 303:
        direction = 'WNW'        
    elif deg >= 304 and deg <= 326:
        direction = 'NW'
    elif deg >= 327 and deg <= 348:
        direction = 'NNW'    

    return(direction)

def windKnots(speed):
    knots = float(speed) * 1.943844
    knots = round(knots, 2)

    return(knots)

def windKmh(speed):
    kmh = float(speed) * 3.6
    kmh = round(kmh, 2)

    return(kmh)

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
                    'degrees' : args['directionV'],
                    'direction' : windDirection(args['directionV']),
                    'speed' : args['speedV'],
                    'knots' : windKnots(args['speedV']),
                    'kmh' : windKmh(args['speedV']),
                }
            },
            upsert=True
        )


class wind_all(Resource):

    def get(self):

        winds = DB['wind_live'].find().sort("name", pymongo.ASCENDING)

        return(jsonify(json.loads(dumps(winds))))