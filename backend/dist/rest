#! /usr/bin/python3.6
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from pyModbusTCP.client import ModbusClient
from flask_cors import CORS

# Initialize flask
app = Flask(__name__)
api = Api(app)
CORS(app)


class Signs(Resource):
    def get(self, ip):
        # Get outputs via modbus on GET request
        c = ModbusClient(host=ip, port=502, auto_open=True, timeout=1)
        try:
            bits = c.read_coils(16, 6)
            outputs = { 
                "all_clear" : bits[0],
                "emergency" : bits[1],
                "lightning" : bits[2],
                "a" : bits[3],
                "b" : bits[4],
                "c" : bits[5]
            }

            # Return a json response
            return(jsonify(outputs))
        except:
            return(False,404)


    def post(self, ip):
        # Parse the form data
        parser = reqparse.RequestParser()
        parser.add_argument("all_clear")
        parser.add_argument("emergency")
        parser.add_argument("lightning")
        parser.add_argument("a")
        parser.add_argument("b")
        parser.add_argument("c")
        args = parser.parse_args()

        # Set output states via modbus
        c = ModbusClient(host=ip, port=502, auto_open=True)
        c.write_single_coil(16, args["all_clear"])
        c.write_single_coil(17, args["emergency"])
        c.write_single_coil(18, args["lightning"])
        c.write_single_coil(19, args["a"])
        c.write_single_coil(20, args["b"])
        c.write_single_coil(21, args["c"])

        # Read the outputs again
        bits = c.read_coils(16, 6)

        return(bits, 201)

    def put(self, name):
        '''
        Not in use, placeholder
        '''
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()


        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return(user, 200)
        
        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return(user, 201)
    
    def delete(self, name):
        '''
        Not in use, placeholder
        '''
        global users
        users = [user for user in users if user["name"] != name]
        return("{} is deleted.".format(name), 200)

# Add signs url, map to Signs class
api.add_resource(Signs, "/sign/<string:ip>")
# Run flask
app.run(debug=True, host='0.0.0.0')