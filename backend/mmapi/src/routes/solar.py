
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
import mysql.connector



# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]


class solar_create(Resource):

    def post(self):

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("name")
        parser.add_argument("location")
        parser.add_argument("ip")
        parser.add_argument("model")

        args = parser.parse_args()

        data = {
            "name": args['name'],
            "location": args['location'],
            "ip": args['ip'],
            "model": args['model'],
        }

        print(data)

        try:
            DB['solar_controllers'].insert_one(data)

            return({'success': True, 'message': 'Created {}'.format(args['name'])})

        except:
            return({'success': False, 'message': 'Failed to create'})


class solar_update(Resource):
    """POST to update solar controller"""

    def post(self):

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("name")
        parser.add_argument("location")
        parser.add_argument("ip")
        parser.add_argument("model")
        parser.add_argument("uid")

        args = parser.parse_args()

        try:
            DB['solar_controllers'].find_one_and_update(
                {
                    "_id": ObjectId(args['uid']),
                },
                {"$set":
                    {
                        "name": args['name'],
                        "location": args['location'],
                        "ip": args['ip'],
                        "model": args['model'],
                    }
                 }
            )

            return({'success': True, 'message': 'Updated {}'.format(args['name'])})

        except:
            return({'success': False, 'message': 'Failed to update'})


class solar_delete(Resource):
    """ DELETE solar document """

    def delete(self, oid):

        if not oid:

            return({'success': False})

        else:
            controller_del_count = DB['solar_controllers'].delete_many(
                {
                    "_id": ObjectId(oid),
                },
            )

            total_del = controller_del_count.deleted_count

            if total_del > 0:
                return({'success': True, 'message': 'Deleted {} objects.'.format(total_del)})
            else:
                return({'success': False, 'message': '{} not found.'.format(oid)})


class solar_controllers(Resource):

    def get(self):
        # Get zone list
        solar_controllers_uid = []
        solar_controllers = DB['solar_controllers'].find().sort(
            "location", pymongo.ASCENDING)

        for controller in solar_controllers:
            try:
                name = controller['name']
            except KeyError:
                name = ''
            try:
                ip = controller['ip']
            except KeyError:
                ip = ''
            try:
                model = controller['model']
            except KeyError:
                model = ''
            try:
                location = controller['location']
            except KeyError:
                location = ''

            solar_controllers_uid.append(
                {
                    'uid': str(controller['_id']),
                    'name': name,
                    'location': location,
                    'ip': ip,
                    'model': model,
                }
            )       
        

        return(jsonify(json.loads(dumps(solar_controllers_uid))))


class solar_data(Resource):

    def get(self):
        # Get zone list
        solar_data = DB['solar_data'].find()
        

        return(jsonify(json.loads(dumps(solar_data))))