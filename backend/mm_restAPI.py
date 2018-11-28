#! /usr/bin/python3.6
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from pyModbusTCP.client import ModbusClient
from flask_cors import CORS
import pymongo
from bson.json_util import dumps
import json

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
        try:
            return(jsonify(json.loads(dumps(alerts))))
        except:
            return(False,404)


class alert_detail(Resource):
    def get(self, ip):

        # Get alert details from database by ip
        alert_document = db['alert_data'].find_one({'ip' : ip})

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
            return(False,404)


    def post(self, ip):

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
        args = parser.parse_args()

        for key in args:
            if args[key] == 'False':
                outputs.append('')
            else:
                outputs.append(1)


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

        args = parser.parse_args()

        print(args)

        # Insert into database
        db['alert'].insert_one(
            {
                "location" : args['alert_location'],
                "ip" : args['alert_ip'],
                "type" : args['alert_type']
            }
        )

        return(201)

class fleet(Resource):
    def get(self):
        # Get all ping data from the pings collection in mongo
        fleet_data = db['fleet_data'].find()

        # Return collection as a massive json
        try:
            return(jsonify(json.loads(dumps(fleet_data))))
        except:
            return(False,404)

class fleet_detail(Resource):
    def get(self, name):
        # Get document with name
        fleet_data = db['fleet_data'].find({'name' : name})

        # Return collection as a massive json
        try:
            return(jsonify(json.loads(dumps(fleet_data))))
        except:
            return(False,404)


# Map URL's to resource classes
api.add_resource(alert, "/alert")
api.add_resource(alert_detail, "/alert/<string:ip>")
api.add_resource(fleet, "/fleet")
api.add_resource(fleet_detail, "/fleet/<string:name>")
api.add_resource(edit, "/edit")

# Run flask
app.run(debug=True, host='0.0.0.0')