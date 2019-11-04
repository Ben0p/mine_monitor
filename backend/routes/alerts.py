from flask_restful import Resource, reqparse

from env.devprod import env
# from env.docker import env
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy
import time
from flask import jsonify
import datetime
from pyModbusTCP.client import ModbusClient


# Initialize mongo connection one time
CLIENT = pymongo.MongoClient('mongodb://{}:{}/'.format(env['mongodb_ip'], env['mongodb_port']))
DB = CLIENT[env['database']]


class alert_all(Resource):
    """GET for alert data"""

    def get(self):
        # Get all sign data from the signs collection in mongo
        alerts = DB['alert_all'].find().sort("name", pymongo.ASCENDING)

        # Return collection as a massive json
        return(jsonify(json.loads(dumps(alerts))))


class alert_display(Resource):
    """GET for alert data"""

    def get(self):
        display_array = []
        trailers = []

        # Get all sign data from the signs collection in mongo
        alerts = DB['alert_all'].find().sort("name", pymongo.ASCENDING)

        # For each alert object
        for alert in alerts:
            # If the alert type is a trailer
            if alert['type'] == 'Trailer':
                # Less than 2 because if it was 3 it would be the next trailer
                if len(trailers) < 2:
                    trailers.append(alert)
                else:
                    trailers.append(alert)
                    combined_trailer = {
                        'type': 'Trailer',
                        'location': trailers[0]['location'],
                        'online': trailers[0]['online'],
                        'modules': [
                            {
                                "_id": trailers[0]['_id'],
                                'zone': trailers[0]['zone'],
                                'b': trailers[0]['b'],
                                'c': trailers[0]['c'],
                            },
                            {
                                "_id": trailers[1]['_id'],
                                'zone': trailers[1]['zone'],
                                'b': trailers[1]['b'],
                                'c': trailers[1]['c'],
                            },
                            {
                                "_id": trailers[2]['_id'],
                                'zone': trailers[2]['zone'],
                                'b': trailers[2]['b'],
                                'c': trailers[2]['c'],
                            }
                        ]
                    }
                    display_array.append(combined_trailer)
                    trailers = []
                    combined_trailer = {}

            # If the alert is not a trailer
            else:
                display_array.append(alert)

        # Return collection as a massive json
        return(jsonify(json.loads(dumps(display_array))))


class alert_detail(Resource):
    """GET for detailed alert data (output states)"""

    def get(self, uid):

        # Get alert details from database by ip
        try:
            alert_document = DB['alert_all'].find_one({'_id': ObjectId(uid)})
            if alert_document == None:
                return({'found': False})
            alert_document['found'] = True
        except:
            return({'found': False})

        # Check if the name is a trailer
        if alert_document['type'] == 'Trailer':
            modules = []
            trailer_modules = DB['alert_all'].find(
                {'location': alert_document['location']})

            bcount = 0
            ccount = 0

            for module in trailer_modules:

                # Get outputs via modbus on GET request
                c = ModbusClient(
                    host=module['ip'], port=502, auto_open=True, timeout=1)

                try:
                    bits = c.read_coils(16, 6)

                    new_module = {
                        'uid': str(module['_id']),
                        'name': module['name'],
                        'zone': module['zone'],
                        'online': module['online'],
                        'rest': module['rest'],
                        'ip': module['ip'],
                        'latency': module['latency'],
                        'b': bits[4],
                        'c': bits[5]
                    }

                    if bits[4]:
                        bcount += 1
                    if bits[5]:
                        ccount += 1

                except:
                    new_module = {
                        'zone': module['zone'],
                        'online': False,
                        'ip': module['ip'],
                        'rest': False,
                        'latency': 999,
                        'b': False,
                        'c': False
                    }

                module_deep_copy = copy.deepcopy(new_module)
                modules.append(module_deep_copy)

            if bcount == 3:
                alert_document['b'] = True
            if ccount == 3:
                alert_document['c'] = True
            alert_document['modules'] = modules

            # Return a json response
            return(jsonify(json.loads(dumps(alert_document))))

        else:
            ip = alert_document['ip']
            c = ModbusClient(host=ip, port=502, auto_open=True, timeout=1)

            try:
                bits = c.read_coils(16, 6)
                alert_document["all_clear"] = bits[0]
                alert_document["emergency"] = bits[1]
                alert_document["lightning"] = bits[2]
                alert_document["a"] = bits[3]
                alert_document["b"] = bits[4]
                alert_document["c"] = bits[5]

            except:
                alert_document["all_clear"] = False
                alert_document["emergency"] = False
                alert_document["lightning"] = False
                alert_document["a"] = False
                alert_document["b"] = False
                alert_document["c"] = False

            return(jsonify(json.loads(dumps(alert_document))))

    def post(self, uid):
        """ POST to control module coil output states """

        # Parse the form data
        parser = reqparse.RequestParser()
        parser.add_argument("type")
        parser.add_argument("output")
        parser.add_argument("state")
        parser.add_argument("ips", action='append')
        args = parser.parse_args()

        outputs = ['all_clear', 'emergency', 'lightning', 'a', 'b', 'c']

        for idx, output in enumerate(outputs):
            if output == args['output']:
                for ip in args['ips']:
                    print(f"{ip}:{output}:{args['state']}")
                    c = ModbusClient(host=ip, port=502,
                                     auto_open=True, timeout=1)
                    coil = idx+16
                    c.write_single_coil(coil, args['state'])

        return(200)


class alert_overview(Resource):
    """GET for alert overview data"""

    def get(self):

        overview = {
            'all_clear': DB['alert_all'].count_documents({'state': 'All Clear'}),
            'emergency': DB['alert_all'].count_documents({'state': 'Emergency'}),
            'a': DB['alert_all'].count_documents({'state': 'A Alert'}),
            'b': DB['alert_all'].count_documents({'state': 'B Alert'}),
            'c': DB['alert_all'].count_documents({'state': 'C Alert'}),
            'offline': DB['alert_all'].count_documents({'state': 'Offline'}),
        }

        # Return collection as a massive json
        return(jsonify(json.loads(dumps(overview))))


class alert_modules(Resource):
    """GET for alert module info"""

    def get(self):
        # try:
        alert_modules_uid = []
        alert_modules = DB['alert_modules'].find().sort(
            "location", pymongo.ASCENDING)

        for alert in alert_modules:
            try:
                zone = alert['zone']
            except KeyError:
                zone = ''
            try:
                ip = alert['ip']
            except KeyError:
                ip = ''
            try:
                location = alert['location']
            except KeyError:
                location = ''
            try:
                _type = alert['type']
            except KeyError:
                _type = ''

            alert_modules_uid.append(
                {
                    'uid': str(alert['_id']),
                    'name': alert['name'],
                    'location': location,
                    'ip': ip,
                    'type': _type,
                    'zone': zone
                }
            )

        # Return collection as a massive json
        return(jsonify(json.loads(dumps(alert_modules_uid))))
        # except:
        #    return(Response(status=418))


class alert_zones(Resource):

    def get(self):
        alert_zones = DB['alert_zones'].find().sort("name", pymongo.ASCENDING)
        alert_zones_list = []

        for zone in alert_zones:
            alert_zones_list.append(
                {
                    'value': zone['name'],
                    'title': zone['name']
                }
            )

        return(jsonify(json.loads(dumps(alert_zones_list))))

class alert_zones_create(Resource):

    def post(self):

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("name")

        args = parser.parse_args()

        try:
            DB['alert_zones'].find_one_and_update(
                {
                    'name':args['name']
                },
                {
                    '$set': {
                        'name' : args['name'],
                    }
                },
                upsert=True
            )

            return({'success': True, 'message': 'Updated {}'.format(args['name'])})

        except:
            return({'success': False, 'message': 'Failed to update'})

class alert_zones_update(Resource):

    def post(self):
        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("name")
        parser.add_argument("uid")

        args = parser.parse_args()

        try:
            DB['alert_zones'].find_one_and_update(
                {
                    "_id": ObjectId(args['uid']),
                },
                {"$set":
                    {
                        "name": args['name'],
                    }
                 }
            )

            return({'success': True, 'message': 'Updated {}'.format(args['name'])})

        except:
            return({'success': False, 'message': 'Failed to update'})

class alert_zones_delete(Resource):

    def post(self):
        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("name")
        parser.add_argument("uid")

        args = parser.parse_args()

        zones_del_count = DB['alert_zones'].delete_many({"name": args['name']})
        zones_del_count = zones_del_count.deleted_count

        if zones_del_count > 0:
            return({'success': True, 'message': f'Deleted {zones_del_count} objects.'})
        else:
            return({'success': False, 'message': f"{args['name']} not found."})

class alert_zones_list(Resource):

    def get(self):
        alert_zones = DB['alert_zones'].find().sort("name", pymongo.ASCENDING)
        alert_zones_list = []

        for zone in alert_zones:
            alert_zones_list.append(
                {
                    'uid': str(zone['_id']),
                    'name': zone['name'],
                }
            )

        return(jsonify(json.loads(dumps(alert_zones_list))))

class alert_types(Resource):

    def get(self):
        alert_types = DB['alert_types'].find().sort("name", pymongo.ASCENDING)
        alert_types_list = []

        for types in alert_types:
            alert_types_list.append(
                {
                    'value': types['name'],
                    'title': types['name']
                }
            )

        return(jsonify(json.loads(dumps(alert_types_list))))


class alert_status(Resource):

    def get(self):
        # Get zone list
        alert_zones = DB['alert_zones'].find()

        # Zone status list
        zone_status = []

        # Retrieve matching alerts in zone
        for zone in alert_zones:
            module_zones = DB['alert_all'].find(
                {
                    'zone': zone['name']
                }
            )

            for alert in module_zones:
                if alert['online']:

                    zone_status.append(
                        {
                            'zone': alert['zone'],
                            'status': alert['status'],
                            'icon': alert['icon'],
                            'state': alert['state'],
                            'online': alert['online']
                        }
                    )
                    break

        return(jsonify(json.loads(dumps(zone_status))))


class alert_create(Resource):

    def post(self):

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("name")
        parser.add_argument("location")
        parser.add_argument("ip")
        parser.add_argument("type")
        parser.add_argument("zone")

        args = parser.parse_args()

        data = {
            "name": args['name'],
            "location": args['location'],
            "ip": args['ip'],
            "type": args['type'],
            "zone": args['zone'],
        }

        try:
            DB['alert_modules'].insert_one(data)

            return({'success': True, 'message': 'Created {}'.format(args['name'])})

        except:
            return({'success': False, 'message': 'Failed to create'})


class alert_update(Resource):
    """POST to update an alert module"""

    def post(self):

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("name")
        parser.add_argument("location")
        parser.add_argument("ip")
        parser.add_argument("type")
        parser.add_argument("zone")
        parser.add_argument("uid")

        args = parser.parse_args()

        try:
            DB['alert_modules'].find_one_and_update(
                {
                    "_id": ObjectId(args['uid']),
                },
                {"$set":
                    {
                        "name": args['name'],
                        "location": args['location'],
                        "ip": args['ip'],
                        "type": args['type'],
                        "zone": args['zone'],
                    }
                 }
            )

            return({'success': True, 'message': 'Updated {}'.format(args['name'])})

        except:
            return({'success': False, 'message': 'Failed to update'})


class alert_delete(Resource):
    """ DELETE alert document """

    def delete(self, name):

        if not name:

            return({'success': False})

        else:
            modules_del_count = DB['alert_modules'].delete_many({"name": name})
            all_del_count = DB['alert_all'].delete_many({"name": name})

            total_del = modules_del_count.deleted_count + all_del_count.deleted_count

            if total_del > 0:
                return({'success': True, 'message': 'Deleted {} objects.'.format(total_del)})
            else:
                return({'success': False, 'message': '{} not found.'.format(name)})