from flask import Flask
from flask_restful import Api, Resource, reqparse
from pyModbusTCP.client import ModbusClient

app = Flask(__name__)
api = Api(app)


class User(Resource):
    def get(self, ip):
        c = ModbusClient(host=ip, port=502, auto_open=True)
        bits = c.read_coils(16, 6)
        return(bits, 200)

    def post(self, ip):

        parser = reqparse.RequestParser()
        parser.add_argument("all_clear")
        parser.add_argument("emergency")
        parser.add_argument("lightning")
        parser.add_argument("a")
        parser.add_argument("b")
        parser.add_argument("c")
        args = parser.parse_args()


        c = ModbusClient(host=ip, port=502, auto_open=True)
        c.write_single_coil(16, args["all_clear"])
        c.write_single_coil(17, args["emergency"])
        c.write_single_coil(18, args["lightning"])
        c.write_single_coil(19, args["a"])
        c.write_single_coil(20, args["b"])
        c.write_single_coil(21, args["c"])

        bits = c.read_coils(16, 6)

        return(bits, 201)

    def put(self, name):
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
        global users
        users = [user for user in users if user["name"] != name]
        return("{} is deleted.".format(name), 200)


api.add_resource(User, "/sign/<string:ip>")
app.run(debug=True, host='0.0.0.0')