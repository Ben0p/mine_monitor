from flask_restful import Resource, reqparse

from env.sol import env

import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
from flask import jsonify, request
import datetime


# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(
    f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]


class weather_wind(Resource):

    def get(self):

        windrose = DB['weather_charts'].find(
            {
                'type': 'windrose',
            }
        )

        return(jsonify(json.loads(dumps(windrose))))
