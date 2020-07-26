
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


class fm_modules(Resource):

    def get(self):
        # Get zone list
        fm_modules = DB['fm_modules'].find().sort("name", pymongo.ASCENDING)
        fm_live = DB['fm_live'].find()

        lives = {}
        for live in fm_live:
            lives[live['module_uid']] = live

        modules = []
        for module in fm_modules:
            data = {
                'location': module['location'],
                'type': module['type'],
                'ip': module['ip'],
                'station': module['station'],
                'url': lives[str(module['_id'])]['url'],
                'uid': str(module['_id'])
            }

            modules.append(data)

        return(jsonify(json.loads(dumps(modules))))


class fm_create(Resource):

    def post(self):

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("station")
        parser.add_argument("type")
        parser.add_argument("location")
        parser.add_argument("ip")
        parser.add_argument("url")

        args = parser.parse_args()

        print(args['station'])

        module_data = {
            "station": args['station'],
            "type": args['type'],
            "location": args['location'],
            "ip": args['ip'],
        }

        #try:
        result = DB['fm_modules'].insert_one(module_data)
        _id = str(result.inserted_id)
        DB['fm_live'].insert_one(
            {
                "station": args['station'],
                "url" : args['url'],
                "module_uid": _id,
            }
        )

        return({'success': True, 'message': f"Created {args['station']}"})

        #except Exception as e:
        #    return({'success': False, 'message': f'{str(e)}'})


class fm_update(Resource):

    def post(self):

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("station")
        parser.add_argument("type")
        parser.add_argument("location")
        parser.add_argument("ip")
        parser.add_argument("url")
        parser.add_argument("uid")

        args = parser.parse_args()

        try:
            DB['fm_modules'].find_one_and_update(
                {
                    "_id": ObjectId(args['uid']),
                },
                {"$set":
                    {
                        "station": args['station'],
                        "type": args['type'],
                        "location": args['location'],
                        "ip": args['ip'],
                    }
                 }
            )
            
            # Update FM live DB
            DB['fm_live'].find_one_and_update(
                {
                    "module_uid": args['uid'],
                },
                {"$set":
                    {
                        "station": args['station'],
                        "url": args['url'],
                    }
                 }
            )

            # If it is an odroid, update it's URL and Station name
            if args['type'] == 'Odroid':
                try:
                    odroid_client = pymongo.MongoClient(f"mongodb://{args['ip']}:{env['mongodb_port']}/")
                    odroid_db = odroid_client['fm_stream']

                    odroid_db['fm_live'].insert_one(
                        {
                            "station": args['station'],
                            "url": args['url'],
                            "changed": time.time()
                        }

                    )
                except:
                    return({'success': False, 'message': f"Unable to update {args['type']} {args['station']}"})


            return({'success': True, 'message': 'Updated {}'.format(args['station'])})

        except Exception as e:
            return({'success': False, 'message': f'{str(e)}'})


class fm_delete(Resource):

    def delete(self, oid):

        if not oid:

            return({'success': False})

        else:
            module_result = DB['fm_modules'].delete_many(
                {
                    "_id": ObjectId(oid),
                },
            )
            live_result = DB['fm_live'].delete_many(
                {
                    "module_uid": oid,
                },
            )

            total_del = module_result.deleted_count + live_result.deleted_count

            if total_del > 0:
                return({'success': True, 'message': 'Deleted {} objects.'.format(total_del)})
            else:
                return({'success': False, 'message': '{} not found.'.format(oid)})
