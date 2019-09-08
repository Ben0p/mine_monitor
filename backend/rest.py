#! /usr/bin/python3.7

# from env.dev import env
# from env.prod import env
from env.devprod import env
from flask import Flask, jsonify, send_file, Response
from flask_restful import Api, Resource, reqparse
from pyModbusTCP.client import ModbusClient
from flask_cors import CORS
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import copy

""" Rest API for alerts
Retrieves data from mongo 
Serves as http json
"""

# Initialize flask
APP = Flask(__name__)
API = Api(APP)
CORS(APP)

# Initialize mongo connection one time
CLIENT = pymongo.MongoClient('mongodb://{}:{}/'.format(env['mongodb_ip'], env['mongodb_port']))
DB = CLIENT[env['database']]


class alert_all(Resource):
    """GET for alert data"""
    def get(self):
        # Get all sign data from the signs collection in mongo
        alerts = DB['alert_all'].find().sort("name",pymongo.ASCENDING)

        # Return collection as a massive json 
        return(jsonify(json.loads(dumps(alerts))))

class alert_display(Resource):
    """GET for alert data"""
    def get(self):
        display_array = []
        trailers = []

        # Get all sign data from the signs collection in mongo
        alerts = DB['alert_all'].find().sort("name",pymongo.ASCENDING)

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
                        'type' : 'Trailer',
                        'location' : trailers[0]['location'],
                        'online' : trailers[0]['online'],
                        'modules' : [
                            {
                                'zone' : trailers[0]['zone'],
                                'b' : trailers[0]['b'],
                                'c' : trailers[0]['c'],
                            },
                            {
                                'zone' : trailers[1]['zone'],
                                'b' : trailers[1]['b'],
                                'c' : trailers[1]['c'],
                            },
                            {
                                'zone' : trailers[2]['zone'],
                                'b' : trailers[2]['b'],
                                'c' : trailers[2]['c'],
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

    def get(self, name):

        # Get alert details from database by ip
        alert_document = DB['alert_data'].find_one({'location': name})
        if alert_document == None:
            return(404)

        # Check if the name is a trailer
        if name[:2] == 'TR':
            west_ip = alert_document['areas'][0]['ip']
            central_ip = alert_document['areas'][1]['ip']
            east_ip = alert_document['areas'][2]['ip']

            # Create list of ips
            ips = [west_ip, central_ip, east_ip]

            
            for index, ip in enumerate(ips):
                # Get outputs via modbus on GET request
                c = ModbusClient(host=ip, port=502, auto_open=True, timeout=1)

                try:
                    bits = c.read_coils(16, 6)
                    alert_document['areas'][index]["all_clear"] = bits[0]
                    alert_document['areas'][index]["emergency"] = bits[1]
                    alert_document['areas'][index]["lightning"] = bits[2]
                    alert_document['areas'][index]["a"] = bits[3]
                    alert_document['areas'][index]["b"] = bits[4]
                    alert_document['areas'][index]["c"] = bits[5]
                
                except: 
                    alert_document['areas'][index]["all_clear"] = False
                    alert_document['areas'][index]["emergency"] = False
                    alert_document['areas'][index]["lightning"] = False
                    alert_document['areas'][index]["a"] = False
                    alert_document['areas'][index]["b"] = False
                    alert_document['areas'][index]["c"] = False

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


    def post(self, name):
        """ POST to control module coil output states """

        # Blank output array
        outputs = []
        trailer_outputs = []

        # Parse the form data
        parser = reqparse.RequestParser()
        parser.add_argument("all_clear")
        parser.add_argument("emergency")
        parser.add_argument("lightning")
        parser.add_argument("a")
        parser.add_argument("b")
        parser.add_argument("c")
        parser.add_argument("ip")
        parser.add_argument("west_b")
        parser.add_argument("west_c")
        parser.add_argument("central_b")
        parser.add_argument("central_c")
        parser.add_argument("east_b")
        parser.add_argument("east_c")

        args = parser.parse_args()

        # False lookup
        false_array = ['False', 'false', '0', False]

        # Get alert details from database by ip
        alert_document = DB['alert_data'].find_one({'location': name})
        if alert_document == None:
            return(404)

        # Check if the name is a trailer
        if name[:2] == 'TR':
            west_ip = alert_document['areas'][0]['ip']
            central_ip = alert_document['areas'][1]['ip']
            east_ip = alert_document['areas'][2]['ip']

            # Create list of ips
            ips = [west_ip, central_ip, east_ip]
            trailer_bits = [
                [args['west_b'], args['west_c']],
                [args['central_b'], args['central_c']],
                [args['east_b'], args['east_c']]
            ]

            for index, ip in enumerate(ips):
                # Get outputs via modbus on GET request
                c = ModbusClient(host=ip, port=502, auto_open=True, timeout=1)
                
                try:

                    # B
                    output_b = trailer_bits[index][0]
                    if output_b in false_array:
                        output_b = ''
                    
                    # C
                    output_c = trailer_bits[index][1]
                    if output_c in false_array:
                        output_c = ''                  

                    # Set B Alert
                    c.write_single_coil(20, output_b)
                    # Set C Alert
                    c.write_single_coil(21, output_c)
                    # Read outputs
                    bits = c.read_coils(16, 6)
                    
                    trailer_outputs.append([bits[4], bits[5]])
                
                except: 
                    trailer_outputs.append([0,0])

            # Return a json response
            return(trailer_outputs)

        else:
            ip = args['ip']
            c = ModbusClient(host=ip, port=502, auto_open=True, timeout=1)
            
            outputs = [args['all_clear'], args['emergency'], args['lightning'], args['a'], args['b'], args['c']]

            for index, output in enumerate(outputs):
                if output in false_array:
                    outputs[index] = ''

            try:
                # Set output states via modbus
                c.write_single_coil(16, outputs[0])
                c.write_single_coil(17, outputs[1])
                c.write_single_coil(18, outputs[2])
                c.write_single_coil(19, outputs[3])
                c.write_single_coil(20, outputs[4])
                c.write_single_coil(21, outputs[5])

                # Read the outputs again
                bits = c.read_coils(16, 6)
            
            except: 
                return(404)
            
            return(bits)

class alert_overview(Resource):
    """GET for alert overview data"""
    def get(self):

        overview = {
            'all_clear' : DB['alert_data'].count_documents({'all_clear':True}),
            'emergency' : DB['alert_data'].count_documents({'emergency': True}),
            'a' : DB['alert_data'].count_documents({'a': True}),
            'b' : DB['alert_data'].count_documents({'b': True}),
            'c' : DB['alert_data'].count_documents({'c': True}),
            'offline' : DB['alert_data'].count_documents({'online': False}),
        }


        # Return collection as a massive json 
        return(jsonify(json.loads(dumps(overview))))

class alert_modules(Resource):
    """GET for alert module info"""
    def get(self):
        #try:
        alert_modules_uid = []
        alert_modules = DB['alert_modules'].find().sort("location",pymongo.ASCENDING)

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
                    'type' : _type,
                    'zone': zone
                }
            )

        # Return collection as a massive json 
        return(jsonify(json.loads(dumps(alert_modules_uid))))
        #except:
        #    return(Response(status=418))

class alert_zones(Resource):

    def get(self):
        alert_zones = DB['alert_zones'].find().sort("name",pymongo.ASCENDING)
        alert_zones_list = []

        for zone in alert_zones:
            alert_zones_list.append(
                {
                    'value': zone['name'],
                    'title': zone['name']
                }
            )

        return(jsonify(json.loads(dumps(alert_zones_list))))

class alert_types(Resource):

    def get(self):
        alert_types = DB['alert_types'].find().sort("name",pymongo.ASCENDING)
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
        
        # Find first matching module for each zone
        for zone in alert_zones:
            module_zone = DB['alert_all'].find_one(
                {
                    'zone': zone['name']
                }
            )


            if module_zone:
                zone_status.append(
                    {
                        'zone' : module_zone['zone'],
                        'status' : module_zone['status'],
                        'icon' : module_zone['icon'],
                        'state' : module_zone['state'],
                        'online' : module_zone['online']
                    }
                )
                        

        return(jsonify(json.loads(dumps(zone_status))))


class alert_edit(Resource):
    """POST to add edit alerts"""

    def post(self):

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Parse arguments from form data
        parser.add_argument("location")
        parser.add_argument("ip")
        parser.add_argument("type")
        parser.add_argument("zone")

        args = parser.parse_args()

        try:
            DB['alert'].find_one_and_update(
                {
                    "ip": args['ip'],
                },
                { "$set":
                    {
                        "location": args['location'],
                        "ip": args['ip'],
                        "type": args['alert_type'],
                        "zone": args['zone'],
                    }
                }
            )

            return(201)

        except:
            return(404)


class alert_delete(Resource):
    """ DELETE alert document """

    def delete(self, name):

        if not name:

            return({'success' : False})

        else:
            modules_del_count = DB['alert_modules'].delete_many({"name" : name})
            all_del_count = DB['alert_all'].delete_many({"name" : name})

            total_del = modules_del_count.deleted_count + all_del_count.deleted_count

            if total_del > 0:
                return({'success' : True, 'message' : 'Deleted {} objects.'.format(total_del)})
            else:
                return({'success' : False, 'message' : '{} not found.'.format(name)})




class check(Resource):
    def get(self):

        response = {'online' : True}

        # Return response
        return(jsonify(json.loads(dumps(response))))


# Map URL's to resource classes
API.add_resource(alert_all, "/alerts/all")
API.add_resource(alert_display, "/alerts/display")
API.add_resource(alert_modules, "/alerts/modules")
API.add_resource(alert_overview, "/alerts/overview")
API.add_resource(alert_zones, "/alerts/zones")
API.add_resource(alert_types, "/alerts/types")
API.add_resource(alert_status, "/alerts/status")
API.add_resource(alert_edit, "/alerts/edit")
API.add_resource(alert_detail, "/alerts/<string:name>")
API.add_resource(alert_delete, "/alerts/delete/<string:name>")
API.add_resource(check, "/check")

# Run flask
APP.run(debug=True, host='0.0.0.0')