#! /usr/bin/python3.6
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from pyModbusTCP.client import ModbusClient
from flask_cors import CORS
import pymongo
from bson.json_util import dumps
import json
import copy


# Initialize flask
app = Flask(__name__)
api = Api(app)
CORS(app)

# Initialize mongo
client = pymongo.MongoClient('mongodb://10.20.64.253:27017/')
db = client['minemonitor']


class alert(Resource):
    def get(self):
        # Get all sign data from the signs collection in mongo
        alerts = db['alert_data'].find()

        # Return collection as a massive json
        return(jsonify(json.loads(dumps(alerts))))


class alert_detail(Resource):
    def get(self, name):

        # Get alert details from database by ip
        alert_document = db['alert_data'].find_one({'location': name})
        if alert_document == None:
            return(404)
        ip = alert_document['ip']

        # Get outputs via modbus on GET request
        c = ModbusClient(host=ip, port=502, auto_open=True, timeout=1)

        try:
            bits = c.read_coils(16, 6)
            alert_document["all_clear"] = bits[0]
            alert_document["emergency"] = bits[1]
            alert_document["lightning"] = bits[2]
            alert_document["a"] = bits[3]
            alert_document["b"] = bits[4]
            alert_document["c"] = bits[5]

            # Return a json response
            return(jsonify(json.loads(dumps(alert_document))))

        except:
            return(False, 404)

    def post(self, name):

        # Blank output array
        outputs = []
        # Parse the form data
        parser = reqparse.RequestParser()
        parser.add_argument("all_clear")
        parser.add_argument("emergency")
        parser.add_argument("lightning")
        parser.add_argument("a")
        parser.add_argument("b")
        parser.add_argument("c")
        parser.add_argument("ip")
        args = parser.parse_args()

        ip = args['ip']

        inputs = [args['all_clear'], args['emergency'], args['lightning'], args['a'], args['b'], args['c']]

        for key in inputs:
            if key == 'False':
                outputs.append('')
            else:
                outputs.append(1)
        print(ip)
        print(outputs)

        # Set output states via modbus
        c = ModbusClient(host=ip, port=502, auto_open=True)
        c.write_single_coil(16, outputs[0])
        c.write_single_coil(17, outputs[1])
        c.write_single_coil(18, outputs[2])
        c.write_single_coil(19, outputs[3])
        c.write_single_coil(20, outputs[4])
        c.write_single_coil(21, outputs[5])

        # Read the outputs again
        bits = c.read_coils(16, 6)

        print(bits)

        return(bits, 201)


class edit(Resource):

    def post(self):
        # Parse the form data
        parser = reqparse.RequestParser()
        parser.add_argument("alert_location")
        parser.add_argument("alert_ip")
        parser.add_argument("alert_type")
        parser.add_argument("type")
        parser.add_argument("west_ip")
        parser.add_argument("central_ip")
        parser.add_argument("east_ip")
        parser.add_argument("trailer_number")

        args = parser.parse_args()

        print(args)

        # Check object type
        if args['type'] == 'alert':
             # Check if document exists
            existing_document = db['alert_data'].find({'location' : args['trailer_number']})
            print('Updating {}'.format(args['trailer_number']))

            # Delete any existing documents
            if existing_document.count() >= 1:
                print('existing document')
                db['alert'].delete_many({'location' : args['trailer_number']})
                db['alert_data'].delete_many({'location' : args['trailer_number']})

            # Check if object is a trailer 
            if args['alert_type'] == 'trailer':
                # Insert into database
                db['alert'].insert_one(
                    {
                        "location": args['trailer_number'],
                        "west_ip": args['west_ip'],
                        "central_ip": args['central_ip'],
                        "east_ip": args['east_ip'],
                        "type": args['alert_type']
                    }
                )

            else:
                # Insert into database
                db['alert'].insert_one(
                    {
                        "location": args['alert_location'],
                        "ip": args['alert_ip'],
                        "type": args['alert_type']
                    }
                )

            return(201)
        else:
            return(404)


class delete(Resource):

    def delete(self, device):

        _type, _device = device.split('-')

        try:
            if _type == 'alert':
                db['alert_data'].delete_one({"ip": _device})
                db['alert'].delete_one({"ip":  _device})

                return(202)
            return(418)

        except:
            return(418)


class fleet(Resource):
    def get(self):
        # Get all ping data from the pings collection in mongo
        fleet_data = db['fleet_data'].find()

        # Return collection as a massive json
        try:
            return(jsonify(json.loads(dumps(fleet_data))))
        except:
            return(False, 404)


class fleet_detail(Resource):
    def get(self, name):
        # Get document with name
        fleet_data = db['fleet_data'].find({'name': name})

        # Return collection as a massive json
        try:
            return(jsonify(json.loads(dumps(fleet_data))))
        except:
            return(False, 404)


# Map URL's to resource classes
api.add_resource(alert, "/alert")
api.add_resource(alert_detail, "/alert/<string:name>")
api.add_resource(fleet, "/fleet")
api.add_resource(fleet_detail, "/fleet/<string:name>")
api.add_resource(edit, "/edit")
api.add_resource(delete, "/edit/<string:device>")

# Run flask
app.run(debug=True, host='0.0.0.0')
