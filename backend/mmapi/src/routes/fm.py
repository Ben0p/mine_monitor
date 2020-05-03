
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



class fm_live(Resource):

    def get(self):
        # Get zone list
        fm_live = DB['fm_live'].find().sort("name", pymongo.ASCENDING)
        
        return(jsonify(json.loads(dumps(fm_live))))