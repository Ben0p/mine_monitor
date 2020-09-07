
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


class ups_create(Resource):

    def post(self):

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("name")
        parser.add_argument("location")
        parser.add_argument("ip")
        parser.add_argument("type")

        args = parser.parse_args()

        data = {
            "name": args['name'],
            "location": args['location'],
            "ip": args['ip'],
            "type": args['type'],
        }

        try:
            DB['ups_modules'].insert_one(data)

            return({'success': True, 'message': 'Created {}'.format(args['name'])})

        except:
            return({'success': False, 'message': 'Failed to create'})


class ups_update(Resource):
    """POST to update solar controller"""

    def post(self):

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("name")
        parser.add_argument("location")
        parser.add_argument("ip")
        parser.add_argument("type")
        parser.add_argument("uid")

        args = parser.parse_args()

        try:
            DB['ups_modules'].find_one_and_update(
                {
                    "_id": ObjectId(args['uid']),
                },
                {"$set":
                    {
                        "name": args['name'],
                        "location": args['location'],
                        "ip": args['ip'],
                        "type": args['type'],
                    }
                 }
            )

            return({'success': True, 'message': 'Updated {}'.format(args['name'])})

        except:
            return({'success': False, 'message': 'Failed to update'})


class ups_delete(Resource):
    """ DELETE solar document """

    def delete(self, oid):

        if not oid:

            return({'success': False})

        else:
            module_del_count = DB['ups_modules'].delete_many(
                {
                    "_id": ObjectId(oid),
                },
            )

            total_del = module_del_count.deleted_count

            if total_del > 0:
                return({'success': True, 'message': 'Deleted {} objects.'.format(total_del)})
            else:
                return({'success': False, 'message': '{} not found.'.format(oid)})


class ups_modules(Resource):

    def get(self):
        # Get solar modules
        ups_modules = DB['ups_modules'].find().sort("location",pymongo.ASCENDING)

        return(jsonify(json.loads(dumps(ups_modules))))


class ups_status(Resource):

    def get(self):

        # Get most recent
        ups_status = DB['ups_data'].aggregate([
            { "$sort": { "unix": -1 } },
            { 
                "$group" : {
                    "_id" : "$module_uid",
                    "unix" : { "$first": "$unix" },
                    "status" : { "$first": "$status" },
                    "phases" : { "$first": "$phases" },
                    "batt_status" : { "$first": "$batt_status" },
                    "batt_icon" : { "$first": "$batt_icon" },
                    "load_percent" : { "$first": "$load_precent" },
                    "load_status" : { "$first": "$load_status" },
                    "load_icon" : { "$first": "$load_icon" },
                    "batt_remaining" : { "$first": "$batt_remaining" },
                    "kw_out" : { "$first": "$kw_out" },
                    "temp" : { "$first": "$temp" },
                    "temp_status" : { "$first": "$temp_status" },
                    "temp_icon" : { "$first": "$temp_icon" },
                }
            }
        ])
        
        return(jsonify(json.loads(dumps(ups_status))))