#! /usr/bin/python3.7

from env.dev import env
# from env.prod import env
from flask import Flask, jsonify, send_file
from flask_restful import Api, Resource, reqparse
from pyModbusTCP.client import ModbusClient
from flask_cors import CORS
import pymongo
from bson.json_util import dumps
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
DB = CLIENT[env['collection']]


class alert(Resource):
    """GET for alert data"""
    def get(self):
        # Get all sign data from the signs collection in mongo
        alerts = DB['alert_data'].find().sort("location",pymongo.ASCENDING)

        # Return collection as a massive json 
        return(jsonify(json.loads(dumps(alerts))))


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



class edit(Resource):
    """POST to add new alerts"""

    def post(self):

        # Initilize request parser
        parser = reqparse.RequestParser()

        # Get type
        parser.add_argument("type")

        # Device parent
        parser.add_argument("parent")

        # Parse the form data (alert)
        parser.add_argument("alert_location")
        parser.add_argument("alert_ip")
        parser.add_argument("alert_type")
        parser.add_argument("west_ip")
        parser.add_argument("central_ip")
        parser.add_argument("east_ip")
        parser.add_argument("trailer_number")

        args = parser.parse_args()

        # Check object type
        if args['type'] == 'alert':

            # Check if trailer or not
            if args['alert_type'] == 'trailer':
                # Set name as trailer number
                name = args['trailer_number']
            else:
                # Set name as location
                name = args['alert_location']

            # Check if document exists
            existing_document = DB['alert_data'].find({'location' : name})
            print('Updating {}'.format(name))

            # Delete any existing documents
            if existing_document.count() >= 1:
                DB['alert'].delete_many({'location' : name})
                DB['alert_data'].delete_many({'location' : name})

            # Check if object is a trailer 
            if args['alert_type'] == 'trailer':
                # Insert into database
                DB['alert'].insert_one(
                    {
                        "location": name,
                        "west_ip": args['west_ip'],
                        "central_ip": args['central_ip'],
                        "east_ip": args['east_ip'],
                        "type": args['alert_type']
                    }
                )

            else:
                # Insert into database
                DB['alert'].insert_one(
                    {
                        "location": name,
                        "ip": args['alert_ip'],
                        "type": args['alert_type']
                    }
                )

            return(201)

        else:
            return(404)


class delete(Resource):
    """ DELETE alert document """

    def delete(self, device):

        # Split string into type and device
        _type, _device = device.split('-')
        if not _device:
            _device = ""
            print("Blank device name")

        try:
            if _type == 'alert':
                db['alert_data'].delete_one({"location": _device})
                db['alert'].delete_one({"location":  _device})

            print("Deleted {} - {}".format(_type, _device))
            return(202)

        except:
            return(418)


class check(Resource):
    def get(self):

        response = {'online' : True}

        # Return response
        return(jsonify(json.loads(dumps(response))))


# Map URL's to resource classes
API.add_resource(alert, "/alert")
API.add_resource(alert_detail, "/alert/<string:name>")
API.add_resource(check, "/check")

# Run flask
APP.run(debug=True, host='0.0.0.0')