
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

        module = {
            "name": args['name'],
            "location": args['location'],
            "ip": args['ip'],
            "type": args['type'],
        }

        try:
            module_uid = DB['ups_modules'].insert_one(module).inserted_id

        except:
            return({'success': False, 'message': 'Failed to create'})


        blank_data = {
            'unix' : time.time(),
            'module_uid' : module_uid,
            'status' : [{
                'status' : "Unknown",
                'system_status' : 'basic',
                'system_icon' : 'question-mark-circle-outline'
            }],
            'batt_remaining' : 0,
            'batt_status' : 'basic',
            'batt_icon' : 'battery-outline',
            'temp_status' : 'basic',
            'temp_icon' : 'thermometer-outline',
            'kw_out' : 0,
            'load_percent' : 0,
            'load_status' : 'basic',
            'load_icon' : 'bulb-outline',
            'phases' : [{
                    'phase_voltage' : 0,
                    'phase_icon' : 'activity-outline',
                    'phase_status' : 'basic'
                }]
        }

        try:
            DB['ups_live'].insert_one(blank_data)
            return({'success': True, 'message': 'Created {}'.format(args['name'])})
        except:
            # Delete the module if the blank data fails to insert (Frontend wigs out)
            DB['ups_modules'].delete_many(
                {
                    "_id": module_uid,
                },
            )
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

            data_del_count = DB['ups_data'].delete_many(
                {
                    "module_uid": ObjectId(oid),
                },
            )

            live_del_count = DB['ups_live'].delete_many(
                {
                    "module_uid": ObjectId(oid),
                },
            )

            total_del = module_del_count.deleted_count + data_del_count.deleted_count + live_del_count.deleted_count

            if total_del > 0:
                return({'success': True, 'message': 'Deleted {} objects.'.format(total_del)})
            else:
                return({'success': False, 'message': '{} not found.'.format(oid)})


class ups_modules(Resource):

    def get(self):
        # Get solar modules
        ups_modules = DB['ups_modules'].find().sort("location",pymongo.ASCENDING)

        return(jsonify(json.loads(dumps(ups_modules))))


class ups_list(Resource):

    def get(self):
        ups_modules = DB['ups_modules'].find().sort("location",pymongo.ASCENDING)

        ups_list = []

        for module in ups_modules:
            ups_module = {
                'ip' : module['ip'],
                'name' : module['name'],
                'location' : module['location'],
                'type' : module['type'],
                'uid' : str(module['_id'])
            }

            ups_list.append(ups_module)

        return(jsonify(json.loads(dumps(ups_list))))

class ups_status(Resource):

    def get(self):


        # Get most recent
        ups_live = DB['ups_live'].find()
        ups_modules = DB['ups_modules'].find()


        modules = {}
        for module in ups_modules:
            modules[str(module['_id'])] = module

        lives = []
        for live in ups_live:
            module_id = str(live['module_uid'])
            live['name'] = modules[module_id]['name']
            live['location'] = modules[module_id]['location']
            live['ip'] = modules[module_id]['ip']
            live['type'] = modules[module_id]['type']
            lives.append(live)

        
        return(jsonify(json.loads(dumps(lives))))