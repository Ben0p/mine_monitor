
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

from tetra.decode import sds



# Initialize mongo connection one time
CLIENT = pymongo.MongoClient(f"mongodb://{env['mongodb_ip']}:{env['mongodb_port']}/")
DB = CLIENT[env['database']]


def reconnectSQL():
    # Initialize mySQL connection
    sql = mysql.connector.connect(
    host=f"{env['tetra_sql_host']}",
    user=f"{env['tetra_sql_user']}",
    passwd=f"{env['tetra_sql_passwd']}",
    database=f"{env['tetra_sql_database']}"
    )

    return(sql)


class tetra_node_all(Resource):

    def get(self,):

        nodes = []

        # Initilize request parser
        parser = reqparse.RequestParser()

        sql = reconnectSQL()
        cursor = sql.cursor()

        # Execute MySQL query
        cursor.execute("SELECT \
            Timestamp, \
            NodeNo, \
            Description, \
            RadioRegMsCount, \
            RadioTsCountIdle, \
            RadioTsCountTotal, \
            RadioTsCountItch, \
            RadioTsCountGtch, \
            RadioTsCountMcch, \
            RadioTsCountScch \
            FROM `nodestatus` \
            WHERE StdBy = '0' \
            AND Description NOT LIKE 'ELI%';"
        )

        myresult = cursor.fetchall()

        for x in myresult:

            ts_used = int(x[5] or 0) - int(x[4] or 0)

            try:
                load = ts_used / int(x[5] or 0) * 100
            except ZeroDivisionError:
                load = 0



            info = {
                'timestamp' : x[0],
                'node_number' : x[1],
                'node_description' : x[2],
                'radio_count' : x[3],
                'ts_idle' : x[4],
                'ts_total' : x[5],
                'ts_in' : x[6],
                'ts_gr' : x[7],
                'ts_mc' : x[8],
                'ts_sc' : x[9],
                'ts_used' : ts_used,
                'load' : round(load)
            } 

            nodes.append(info)


        return(jsonify(json.loads(dumps(nodes))))


class tetra_node_load(Resource):

    def get(self):
        # Get zone list
        node_loads = DB['tetra_node_load'].find_one(
            {
                'type': 'bar'
            }
        )

        return(jsonify(json.loads(dumps(node_loads))))


class tetra_node_subscribers(Resource):

    def get(self):
        # Get zone list
        node_loads = DB['tetra_node_subscribers'].find_one(
            {
                'type': 'bar'
            }
        )

        return(jsonify(json.loads(dumps(node_loads))))


class tetra_ts_load(Resource):

    def get(self):
        # Get zone list
        ts_loads = DB['tetra_node_load'].find_one(
            {
                'type': 'radar'
            }
        )
 
        return(jsonify(json.loads(dumps(ts_loads))))

class tetra_radio_count(Resource):

    def get(self, node):
        # Get zone list
        radio_count = DB['tetra_radio_count'].find_one(
            {
                'node': node
            }
        )
 
        return(jsonify(json.loads(dumps(radio_count))))


class tetra_subscribers(Resource):

    def get(self,):

        # Get subscriber list (all)
        subscribers = DB['tetra_subscribers'].find({}, {'_id': False}).sort("ssi", pymongo.ASCENDING)
 
        return(jsonify(json.loads(dumps(subscribers))))


class tetra_call_stats(Resource):

    def get(self, call_type, range_sec):

        # Get subscriber list (all)
        stats = DB['tetra_call_stats'].find_one(
            {
                'type' : call_type,
                'range_sec' : range_sec
            },
            {'_id': False})
 
        return(jsonify(json.loads(dumps(stats))))

class tetra_call_history(Resource):

    def get(self, time_range):

        # Get subscriber list (all)
        stats = DB['tetra_call_stats'].find_one(
            {
                'type' : 'history',
                'range' : time_range
            },
            {'_id': False})
 
        return(jsonify(json.loads(dumps(stats))))


class tetra_subscriber_detail(Resource):

    def get(self, issi):

        sql = reconnectSQL()
        cursor = sql.cursor()
        
        # Execute MySQL query
        cursor.execute(f"SELECT \
            Timestamp, \
            OriginatingNodeNo, \
            UserDataLength, \
            Rssi, \
            MsDistance, \
            UserData \
            FROM sdsdata \
            WHERE CallingSsi = {issi} \
            AND UserDataLength = 129 \
            ORDER BY Timestamp \
            DESC LIMIT 1;"
        )

        myresult = cursor.fetchall()

        # Placeholder default values
        detail = {
            'timestamp' : 'None',
            'node' : 'None',
            'gps' : False,
            'rssi' : 'None',
            'distance' :'None',
            'location' : {
                'location' : {
                    'latitude' : {
                        'decimal_degrees' : 'None',
                        'meridian' : ''
                    },
                    'longitude' : {
                        'decimal_degrees' : 'None',
                        'meridian' : ''
                    },
                    'altitude' : {
                        'meters' : 'None'
                    },
                    'uncertainty' : 'None'
                },
                'velocity' : {
                    'kmh' : 'None'
                },
                'time' : {
                    'local' : 'None'
                },
            }
        }


        try:
            hex_string = myresult[0][5].hex()
            hex_string = hex_string.rstrip("0")
            location = sds(str(hex_string))
            lat = location['location']['latitude']['decimal_degrees']
            lon = location['location']['longitude']['decimal_degrees']
            maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            location['location']['maps_url'] = maps_url

            time = myresult[0][0] + datetime.timedelta(hours=8)
            time = time.strftime('%d/%m/%Y %H:%M:%S')

            node_name = DB['tetra_nodes'].find_one(
                {
                    'node_number' : myresult[0][1],
                },
                {'_id': False}
            )

            if myresult[0][2] ==  129:
                gps = True
            elif myresult[0][2] == 44:
                gps = False



            detail = {
                'timestamp' : time,
                'node' : node_name['node_description'],
                'gps' : gps,
                'rssi' : myresult[0][3] * -1,
                'distance' : myresult[0][4],
                'location' : location
            }
        except IndexError:
            return(detail)

 
        return(jsonify(json.loads(dumps(detail))))